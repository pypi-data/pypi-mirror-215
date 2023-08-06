# coding: utf8

from enum import unique
from ...._base_enum import StrEnum


@unique
class SettlementType(StrEnum):
    ASSET = "Asset"
    CASH = "Cash"
    PHYSICAL = "Physical"
    UNDEFINED = "Undefined"
