from enum import unique
from .._base_enum import StrEnum


@unique
class TenorTypes(StrEnum):
    ODD = "Odd"
    LONG = "Long"
    IMM = "IMM"
    BEGINNING_OF_MONTH = "BeginningOfMonth"
    END_OF_MONTH = "EndOfMonth"
