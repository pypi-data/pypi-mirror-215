import pandas as pd
import numpy as np
import wbdata as wb
import json

from tinydb import TinyDB, where, Query 
from enum import Enum
from operator import and_, or_
from functools import reduce
from typing import Self, Any, Generator, Union, Literal
from itertools import chain
from urllib.parse import urljoin
from rich.progress import (
    Progress, SpinnerColumn, TextColumn, TimeElapsedColumn, Task,
    BarColumn
    )
from rich.console import Console
from rich.table import Table

from typer_tinydb.utils import renderQuery
import wbdata as wb
import json
from openborders.utils import Root, Pkg, Data, enumFromDict
from openborders.data import DataSource, Dimensions, DIMS_DB, GDIM_URL

console = Console()
log = console.log

spinner = Progress(
    SpinnerColumn(),
    "[progress.description]{task.description}",
    "•",
    BarColumn(),
    "•",
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    TimeElapsedColumn()
)
"""A rich spinner for loading display"""

__all__ = [
    "spinner",
    "DataIndex"
]

def isCacheComplete(db: TinyDB) -> bool:
    """Checks if cache is complete given the analysis dimensions provided by `openborders.data.Dimensions.All`

    Args:
        db (TinyDB): The local cache data, stored in a `.json` TinyDB instance of a few MBs.

    Returns:
        bool: Whether one dimension misses. False if one is not present.
    """
    dims = map(lambda doc: doc['id'], db.all())
    if next(dims, None) is None:
        return False
    absdims = filter(lambda v: v not in [m.value for m in Dimensions.All], dims)
    item = next(absdims, None)
    return item is None

class DataIndex:
    """A data Index, represents the actual collection of every row for each dimension used to create the overall metric.

    Returns:
        DataIndex: A class that interfaces between the raw cached data and formats such as pandas' `pd.DataFrame`. 
    """
    Dimensions = Dimensions
    
    def __new__(cls, dropna: bool = True) -> Self:
        """Initializes the index, downloading successive dimensions from the corresponding APIs.

        Args:
            dropna (bool, optional): Whether to drop NA rows for each index. Can result in missing year/country pairs. Defaults to True.

        Returns:
            Self: `DataIndex` reflecting the downloaded content
        """
        cls.db = DIMS_DB()
        cls.df = None
        spinner.start()
        cache = spinner.add_task("Checking cache..")
        if isCacheComplete(cls.db):
            spinner.remove_task(cache)
            return cls
        spinner.remove_task(cache)
        for dim in spinner.track(cls.Dimensions.All, description="Loading indicators..."):
            n = dim.name
            v = dim.value
            if not cls.db.contains(where('id') == v):
                tk = spinner.add_task(f"Downloading data for {n} ({v})", total=None)
                ds = DataSource.from_identifier(v)
                df = ds.fetch()
                if dropna:
                    df = df.dropna()
                doc = {
                    'records': df.to_dict(orient='records'),
                    'indicator' : n,
                    'id': v,
                    'source_name' : ds.name,
                    'source_origin' : ds.dtype,
                    'source_full_name': ds.full_name
                }
                cls.db.upsert(doc, where('id') == v)
                spinner.remove_task(tk)
        spinner.stop()
        return cls
    
    @classmethod
    def wipe(cls):
        """Truncates the underlying cache, emptying all memory of downloaded content.
        """
        cls.db.truncate()
                
    @classmethod
    def to_rich_table(cls, name: str = None, ind_id: str = None) -> Table:
        """Renders the database to a rich table using `rich.table.Table`. Very expensive, low-use overall.

        Args:
            name (str, optional): Indicator on which to filter before rendering. Defaults to None.
            ind_id (str, optional): Indicator identifier on which to filter, of the form <ID>://<route>. Defaults to None.

        Returns:
            rich.table.Table: Rich object to display the cached data in the terminal. 
        """
        if name:
            data = cls.db.search(where('indicator') == name)
            return renderQuery(data, first='indicator', last='indicator_value')
        elif ind_id:
            data = cls.db.search(where('source_full_name') == ind_id)
            return renderQuery(data, first='indicator', last='indicator_value')
        else:
            data = cls.db.all()
            return renderQuery(data, first='indicator', last='indicator_value')
        
    @classmethod
    def to_df(cls, name: str = None, ind_id: str = None) -> pd.DataFrame:
        """Merges every metric and its rows into a single consolidated dataframe.

        Args:
            name (str, optional): Indicator on which to filter before rendering. Defaults to None.
            ind_id (str, optional): Indicator identifier on which to filter, of the form <ID>://<route>. Defaults to None.

        Returns:
            pd.DataFrame: A dataframe of several hundred thousand rows containing every metric.
        """
        if name:
            data = cls.db.search(where('indicator') == name)
            cls.df = pd.DataFrame.from_records(data=data)
        elif ind_id:
            data = cls.db.search(where('id') == ind_id)
            cls.df = pd.DataFrame.from_records(data=data)
        else:
            spinner.start()
            mrg = spinner.add_task("Merging all cached rows..", total=None)
            ftch = spinner.add_task("Fetching all rows..", total=None)
            data = cls.db.all()
            spinner.remove_task(ftch)
            nrows = len(data)
            spinner.update(mrg, total=nrows)
            dfs = []
            for dt in spinner.track(data, total=len(data), description="Merging.."):
                df = pd.DataFrame.from_records(data=dt['records'])
                df['indicator'] = dt['indicator']
                df['indicator_id'] = dt['id']
                dfs += [df]
            spinner.remove_task(mrg)
            concat = spinner.add_task("Concatenation step...", total=None)
            cls.df = pd.concat(dfs, axis=0)
            spinner.remove_task(concat)
            spinner.stop()
        return cls.df
    
    @classmethod
    def preprocess(
        cls,
        dropna: bool = True, 
        list_indicators: bool = False,
        indicator: str = None,
        normalize: bool = True,
        year_gt: int = 1980,
        debug: bool = False
        ) -> pd.DataFrame | str:
        """Preprocesses the merged dataframe by grouping the metrics per batches of 5 years,
        and normalizes the values across countries on that time period.

        Args:
            dropna (bool, optional): Whether to drop NA rows. Defaults to True.
            list_indicators (bool, optional): Whether to just list indicators instead of pre-processing. Defaults to False.
            indicator (str, optional): Whether to filter on a specific indicator before pre-processing. Defaults to None.
            normalize (bool, optional): Whether to perform cross-country normalization of the metrics. Defaults to True.
            year_gt (int, optional): Whether to drop years before a certain date. Defaults to 1980, dropping all years before that date.
            debug (bool, optional): Whether to log additionnal information, verbosity level. Defaults to False.

        Returns:
            pd.DataFrame | str: A preprocessed `pd.DataFrame` ready for use (storage | plotting | ranking)
        """
        if cls.df is None:
            cls.to_df()
        if year_gt:
            cls.df.year = pd.to_datetime(cls.df.year)
            year_gt = pd.to_datetime(f"01-01-{year_gt}", dayfirst=True)
            v = cls.df[cls.df.year >= year_gt].copy()
        if list_indicators:
            v = cls.df.indicator.unique()
            v = ' (+) ' + '\n (+) '.join(v)
        elif indicator:
            v = cls.df[cls.df.indicator == indicator]
        else:
            v = cls.df        

        if normalize:
            spinner.start()
            years = pd.date_range(v.year.min(), v.year.max(), freq='5Y')
            nints = len(years) - 1
            intervals = zip(years, years[1:])
            indicators = v.indicator.unique()
            normalizing = spinner.add_task("[bold red]Normalizing data 📊[/bold red]", total=len(indicators)*nints)
            newcols = ['min', 'max', 'mean', 'std', 'norm_value', 'minmax_value']
            
            for nc in newcols:
                v[nc] = pd.NA
            for start, stop in spinner.track(intervals, nints, description="[bold magenta]Normalizing per period..[/bold magenta]"):
                intv = spinner.add_task(f"[yellow] Interval: {start:%d.%m.%Y} <= dt <= {stop:%d.%m.%Y} [/yellow]", total=len(indicators))
                for ind in indicators:
                    indt = spinner.add_task(f"Indicator: {ind}", total=None)
                    colfilter = (v.year <= stop) & (v.year >= start) & (v.indicator == ind)
                    indval = v.loc[colfilter, 'indicator_value']
                    indval = indval.apply(lambda v: np.nan if v == '' else float(v)).dropna()

                    vmax, vmin, mean, std = indval.max(), indval.min(), indval.mean(), indval.std()
                    rg = vmax - vmin
                    minmax = (indval - vmin) / (rg+1e-09)
                    zscore = (indval - mean) / (std+1e-09)
                    newvals = [vmin, vmax, mean, std, zscore, minmax]
                    
                    if debug:
                        console.log(f"Interval: {start} <= dt <= {stop} | Values: {vmin} <= v <= {vmax} | Z-score: v ≈ μ ± σ ≈ {mean:.2f} ± {std:.2f}")
                    
                    for nc, nv in zip(newcols, newvals):
                        v.loc[colfilter, nc] = nv
                    spinner.update(normalizing, advance=1)
                    spinner.update(intv, advance=1)
                    spinner.refresh()
                    spinner.remove_task(indt)
                spinner.remove_task(intv)
            spinner.remove_task(normalizing)
            
        if dropna:
            v = v.dropna()
            
        return v
    