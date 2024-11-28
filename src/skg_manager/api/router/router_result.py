import typing as t
from dataclasses import dataclass
from enum import Enum


@dataclass
class Result:
    class Status(Enum):
        SUCCESS = 0
        FAILURE = 1
        NOT_IMPLEMENTED = 2

    status: Status
    message: str
    data: t.Any = None
