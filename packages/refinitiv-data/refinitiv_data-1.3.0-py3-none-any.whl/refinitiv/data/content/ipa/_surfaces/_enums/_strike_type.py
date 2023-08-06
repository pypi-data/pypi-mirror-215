from enum import Enum, unique


@unique
class StrikeType(Enum):
    ABSOLUTE_PERCENT = "AbsolutePercent"
    RELATIVE_PERCENT = "RelativePercent"
