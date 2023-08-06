import json
import pandas as pd
from enum import Enum
from pathlib import Path
from itertools import chain
from tinydb import TinyDB, where, Query 
from typing import Self, Any, Generator, Union, Literal

from rich.console import Console
from rich.table import Table

from typer_tinydb.utils import renderQuery
import wbdata as wb
import json
from openborders.utils import Root, Pkg, Data, enumFromDict

__all__ = [
    "DataSource",
    "DIMS_DB_PATH",
    "DIMS_DB",
    "GDIM_URL",
    "GDIM_COLUMNS_PATH",
    "GDIM_PREFIX",
    "WB_PREFIX",
    "T_YOS",
    "T_RANK",
    "T_CAT",
    "T_ANY",
    "MobilityMetrics",
    "Immigration",
    "Education",
    "Labor",
    "Wages",
    "Business",
    "DataSource"
]

DIMS_DB_PATH = Data / 'dims.json'
DIMS_DB = lambda: TinyDB(DIMS_DB_PATH)
GDIM_URL = "https://datacatalogfiles.worldbank.org/ddh-published/0050771/DR0065670/GDIM_2023_03.csv"
GDIM_COLUMNS_PATH = Data / 'gdim.columns.json'
GDIM_PREFIX = "GDIM://"
WB_PREFIX = "WB://"

T_YOS = Literal['years_of_schooling']
T_RANK = Literal['rank']
T_CAT = Literal['category']
T_ANY = Union[T_RANK, T_CAT, T_YOS]


class SourcePrefix(str):
    """Represents a source using a file-like prefix. WB://<id> means the id points to a World Bank id, etc.

    Args:
        str (_type_): Inherits from `str`, just a glorified prefix string.

    Returns:
        SourcePrefix: A prefixed string class 
    """
    P_GDIM = GDIM_PREFIX
    P_WB = WB_PREFIX
    PREFIX = None
    ROUTE = None
    ORIGIN = None
    
    @classmethod
    def WB(cls) -> Self:
        """Adds the World Bank Prefix to the object

        Returns:
            Self: A `SourcePrefix` instance with Prefix set to `WB://`
        """
        cls.PREFIX = cls.P_WB
        cls.ORIGIN = 'WB'
        return cls
    
    @classmethod
    def GDIM(cls) -> Self:
        """Adds the World Bank's GDIM Prefix to the object

        Returns:
            Self: A `SourcePrefix` instance with Prefix set to `GDIM://`
        """
        cls.PREFIX = cls.P_GDIM
        cls.ORIGIN = 'GDIM'
        return cls
    
    @classmethod
    def __matmul__(cls, route: str) -> Self:
        """Equivalent of `at`, bases the route at the previously set prefix value.

        Args:
            route (str): A route / id that points to a subset within the prefix

        Returns:
            Self: A `SourcePrefix` instance with Prefix & route set.
        """
        cls.ROUTE = cls.PREFIX + route
        return cls
    
    def __new__(cls, prefix: str = None) -> Self:
        """Creates a new`SourcePrefix` from a prefix string

        Args:
            prefix (str, optional): prefix type, case insensitive, 'wb' leads to prefix `WB://` etc. Defaults to None.

        Returns:
            Self: A `SourcePrefix` instance with Prefix set.
        """
        if not prefix:
            return cls
        if 'wb' in prefix.lower():
            return cls.WB()
        elif 'gdim' in prefix.lower() :
            return cls.GDIM()
        else:
            return cls.WB()
    
    @classmethod
    def at(cls, route: str) -> Self:
        """Equivalent of `Self @ route`, bases the route at the previously set prefix value.

        Args:
            route (str): A route / id that points to a subset within the prefix

        Returns:
            Self: A `SourcePrefix` instance with Prefix & route set.
        """
        cls.ROUTE = cls.PREFIX + route
        return cls
    
    @classmethod
    def eval(cls) -> str:
        """Evaluates the SourcePrefix to yield the entire identifier `<prefix><route>` or `<ID>://<route>`

        Returns:
            str: the full identifier
        """
        return cls.ROUTE
    
    @classmethod
    def prefix(cls) -> str:
        """A simple getter to retrieve the underlying prefix.

        Returns:
            str: the prefix used by the class
        """
        return cls.PREFIX
    
    @staticmethod
    def from_pair(prefix:str, route: str) -> Self:
        """Creates immediately the built object from the `prefix` & `source` pair

        Args:
            prefix (str): prefix as string, case insensitive.
            route (str): route to be used from the prefix.

        Returns:
            Self: A `SourcePrefix` instance with Prefix & route set.
        """
        return SourcePrefix(prefix=prefix).at(route=route)
    
    @staticmethod
    def eval_pair(prefix:str, route: str) -> str:
        """Creates and immediately evaluates the built object from the `prefix` & `source` pair

        Args:
            prefix (str): prefix as string, case insensitive.
            route (str): route to be used from the prefix.

        Returns:
            str: A full identifier in string form `<ID>://<route>` 
        """
        return SourcePrefix(prefix=prefix).at(route=route).eval()
    
    @classmethod
    def normalize(cls, full_name: str) -> Self:
        """Sets the route from a full identifier

        Args:
            full_name (str):  A full identifier in string form `<ID>://<route>` 

        Returns:
            Self: A `SourcePrefix` instance with Prefix & route set.
        """
        cls.ROUTE = full_name.removeprefix(cls.PREFIX)
        return cls
    
    @classmethod
    def from_identifier(cls, full_name: str) -> Self:
        """End to end setter from full identifier.

        Args:
            full_name (str): A full identifier in string form `<ID>://<route>` 

        Returns:
            Self: A `SourcePrefix` instance with Prefix & route set.
        """
        if full_name.lower().startswith(cls.P_GDIM.lower()):
            return SourcePrefix().GDIM().normalize(full_name)
        elif full_name.lower().startswith(cls.P_WB.lower()):
            return SourcePrefix().WB().normalize(full_name)
        else:
            return SourcePrefix().WB().normalize(full_name)
        
    @classmethod
    def route(cls):
        """Simple getter for the `route` value

        Returns:
            str: The route from prefix
        """
        return cls.ROUTE

class MobilityMetrics(Enum):
    """All the social mobility metrics from the World Bank's GDIM database.

    Args:
        Enum (_type_): Types of metrics (rank / yos / category)
    """
    RANK = SourcePrefix.eval_pair(GDIM_PREFIX, 'rank')
    YEARS_OF_SCHOOLING = SourcePrefix.eval_pair(GDIM_PREFIX, 'years_of_schooling')
    CATEGORY = SourcePrefix.eval_pair(GDIM_PREFIX,  'category')

class Immigration(Enum):
    """Statistics pertaining to immigration or population

    Args:
        Enum (_type_): Types of statistics
    """
    PERCENT_POPULATION = SourcePrefix.eval_pair(WB_PREFIX,  "SM.POP.TOTL.ZS")
    PERCENT_SLUMS = SourcePrefix.eval_pair(WB_PREFIX,  "EN.POP.SLUM.UR.ZS")
    PERCENT_YOUNG = SourcePrefix.eval_pair(WB_PREFIX,  "SP.POP.DPND.YG")
    
class Labor(Enum):
    """Statistics pertaining to labour and labour quality
    Args:
        Enum (_type_): Types of statistics
    """
    PERCENT_UNEMPLOYMENT = SourcePrefix.eval_pair(WB_PREFIX,  "SL.UEM.TOTL.ZS")
    PERCENT_VULNERABLE_EMPLOYMENT = SourcePrefix.eval_pair(WB_PREFIX,  "SL.EMP.VULN.ZS")
    
class Education(Enum):
    """Statistics pertaining to education

    Args:
        Enum (_type_): Types of statistics
    """
    CHILDREN_UNSCHOOLED = SourcePrefix.eval_pair(WB_PREFIX,  "SE.PRM.UNER.ZS")
    
class Wages(Enum):
    """Statistics pertaining to wages

    Args:
        Enum (_type_): Types of statistics
    """
    GROWTH_RATE_CONSUM_INCOME_PER_CAPITA = SourcePrefix.eval_pair(WB_PREFIX,  "SI.SPR.PCAP.ZG")
    INCOME_SHARE_LOWEST_TWENTY_PCT = SourcePrefix.eval_pair(WB_PREFIX,  "SI.DST.FRST.20")
    POVERTY_RATIO_NATL_LINE = SourcePrefix.eval_pair(WB_PREFIX,  "SI.POV.NAHC")
    
class Business(Enum):
    """Statistics pertaining to ease of doing business

    Args:
        Enum (_type_): Types of statistics
    """
    SHARE_FIRMS_LOSS_THEFT = SourcePrefix.eval_pair(WB_PREFIX,  "IC.FRM.THEV.ZS")
    
class Dimensions:
    """A class regrouping all different statistics and dimensions across which a country should be ranked.
    """
    Labor = Labor
    Wages = Wages
    Education = Education
    Immigration = Immigration
    MobilityMetrics = MobilityMetrics
    All = enumFromDict('All', { m.name : m.value for m in chain(Labor, Wages, Education, Immigration, MobilityMetrics) })

class DataSource:
    """Represents a data source, as identified by a `SourcePrefix`.
    The `DataSource` is able to check and fetch remote data based on the prefixes.
    """
    def __new__(cls, full_name: str) -> Self:
        cls.src = SourcePrefix.from_identifier(full_name=full_name)
        cls.dtype = cls.src.normalize(full_name=full_name).prefix()
        cls.full_name = full_name
        cls.name = cls.src.route()
        return cls
    
    @classmethod
    def as_gdim(cls) -> Self:
        cls.full_name = SourcePrefix.eval_pair(GDIM_PREFIX,  cls.name)
        cls.dtype = 'GDIM'
        return cls
    
    @classmethod
    def as_wb(cls) -> Self:
        cls.full_name = SourcePrefix.eval_pair(WB_PREFIX,  cls.name)
        cls.dtype = 'WB'
        return cls
    
    @classmethod
    def is_wb(cls):
        return 'wb' in cls.dtype.lower()

    @classmethod
    def is_gdim(cls):
        return 'gdim' in cls.dtype.lower()
    
    @staticmethod
    def from_identifier(full_name: str) -> Self:
        ds = DataSource(full_name)
        return ds
            
    @classmethod
    def fetch(cls) -> pd.DataFrame:
        if cls.is_gdim():
            return gdimget(cls.name)
        elif cls.is_wb():
            return wbget(cls.name)
        
    @classmethod
    def __str__(cls) -> str:
        return f"{cls.dtype} @ {cls.full_name} | name = {cls.name}"

def unnest(d: dict) -> dict:
    return list(pd.json_normalize(d).T.to_dict().values()).pop()
            
def gdimInfo(keys: list = None) -> dict:
    gdim_cols = json.loads(GDIM_COLUMNS_PATH.read_text())
    colinfo = unnest(gdim_cols)
    rows = []
    for k,v in colinfo.items():
        row = {}
        add = False
        for _k in keys:
            if _k in k:
                add = True
                row["key"] = k
                row["value"] = v
                if 'match' in row:
                    row['match'] += [_k]
                else:
                    row['match'] = [_k]
        if add:
            rows += [row]
    return rows

def gdimget(names: str) -> pd.DataFrame:
    candidates = []
    for name in names:
        matches = gdimInfo(keys=[name])
        candidates += matches
    metrics = list(filter(lambda itm: itm['key'].endswith('.name'), candidates))
    descs = list(filter(lambda itm: itm['key'].endswith('.description'), candidates))
    df = pd.read_csv(GDIM_URL)
    columns = ['country', 'code', 'year']
    DFs = []
    for d,m in zip(descs,metrics):
        mv = m['value']
        _cols = [*columns, mv]
        dfv = df[_cols].copy()
        dfv.rename(columns={mv:"indicator_value"},inplace=True)
        dfv['indicator_id'] = mv
        dfv["indicator_description"] = d
        dfv['isocode'] = ''
        DFs +=[dfv]
    merge_columns = columns + ['isocode', 'indicator_id', 'indicator_value', 'indicator_description']
    
    return pd.concat([_df[merge_columns].copy() for _df in DFs])

def countryFilter(row):
    n = 'country.value'
    i = 'country.id'
    name = row[n].lower()
    condition = (
        'africa' in name or
        'euro' in name or
        'income' in name or
        'middle east' in name or
        'america' in name or
        'only' in name or
        'total' in name or
        'asia' in name or
        'dividend' in name or
        'countr' in name or
        'debt' in name or
        'state' in name or
        'world' in name or
        'oecd' in name or
        'situation' in name or
        'blend' in name or
        'classified' in name
        )
    return not condition

def wbget(indicator: str) -> pd.DataFrame:
    df = pd.json_normalize(wb.get_data(indicator=indicator))
    nmap = {
        "country.value":"country",
        "country.id":"code",
        "countryiso3code": "isocode",
        "indicator.id":"indicator_id",
        "indicator.value":"indicator_description",
        "date":"year",
        "value":"indicator_value"
    }
    df = df[df.apply(countryFilter, axis=1)].copy()
    df.rename(columns=nmap, inplace=True)
    columns = [
        "country",
        "code",
        "year",
        "indicator_id",
        "indicator_value",
        "indicator_description"
    ]
    return df[columns].copy().fillna('')

