# coding: utf8

from enum import unique
from refinitiv.data._base_enum import StrEnum


@unique
class UnderlyingType(StrEnum):
    """
    The possible values are:
        - Eti: eti(exchanged traded instruments) options,
        - Fx: fx options.
    """

    ETI = "Eti"
    FX = "Fx"
