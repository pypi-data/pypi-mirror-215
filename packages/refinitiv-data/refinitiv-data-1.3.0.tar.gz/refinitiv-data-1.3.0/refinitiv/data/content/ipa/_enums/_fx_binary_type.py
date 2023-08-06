# coding: utf8

from enum import unique
from ...._base_enum import StrEnum


@unique
class FxBinaryType(StrEnum):
    DIGITAL = "Digital"
    NO_TOUCH = "NoTouch"
    NONE = "None"
    ONE_TOUCH_DEFERRED = "OneTouchDeferred"
    ONE_TOUCH_IMMEDIATE = "OneTouchImmediate"
