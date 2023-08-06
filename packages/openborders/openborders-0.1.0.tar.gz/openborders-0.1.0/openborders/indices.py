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

__all__ = [
    "spinner",
    "DataIndex"
]

def isCacheComplete(db):
    dims = map(lambda doc: doc['id'], db.all())
    if next(dims, None) is None:
        return False
    absdims = filter(lambda v: v not in [m.value for m in Dimensions.All], dims)
    item = next(absdims, None)
    return item is None

class DataIndex:
    Dimensions = Dimensions
    
    def __new__(cls, dropna: bool = True) -> Self:
        cls.db = DIMS_DB()
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
        cls.df = None
        cls.aggs = None
        return cls
    
    @classmethod
    def wipe(cls):
        cls.db.truncate()
                
    @classmethod
    def to_rich_table(cls, name: str = None, ind_id: str = None) -> Table:
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
    def preprocess(cls) -> Self:
        if cls.df is not None:
            cls.to_df()
        gbcols = ["country", "year", "indicator"]
        vcols = ["indicator_value"]
        v = "indicator_value"
        cls.df["year"] = pd.to_datetime(cls.df.year)
        cls.df[v] = cls.df[v].str.replace('', 'NaN').astype(float).fillna(method='backfill').fillna(method='ffill').ewm(alpha=0.99).mean()
        cols = gbcols + vcols
        aggs = cls.df[cols].groupby(gbcols).agg({
            v: np.median,
            v: np.std,
            v: np.mean,
            v: np.min,
            v: np.max,
            v: lambda arr : np.quantile(arr, q=0.25),
            v: lambda arr : np.quantile(arr, q=0.75),
        })
        cls.aggs = aggs.reset_index()
        return cls
    