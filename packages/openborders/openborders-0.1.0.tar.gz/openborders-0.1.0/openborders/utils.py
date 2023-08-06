from pathlib import Path
from enum import Enum

__all__ = ["Pkg", "Root", "Data", "enumFromDict"]

Pkg = Path(__file__).parent
Root = Pkg.parent
Data = Root / 'data'

def enumFromDict(name, values):
    _k = _v = None
    class SomeEnum(Enum):
        nonlocal _k, _v
        for _k, _v in values.items():
            locals()[_k] = _v
    SomeEnum.__name__ = name
    return SomeEnum