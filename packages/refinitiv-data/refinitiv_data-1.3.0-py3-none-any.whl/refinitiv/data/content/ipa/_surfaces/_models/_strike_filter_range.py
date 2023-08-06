__all__ = ["StrikeFilterRange"]

from typing import TYPE_CHECKING

from ..._object_definition import ObjectDefinition


if TYPE_CHECKING:
    from ....._types import OptFloat


class StrikeFilterRange(ObjectDefinition):
    """
    StrikeFilterRange for surface.

    Parameters
    ----------
    max_of_median_implied_vol_percent : float, optional
        The value can be used to exclude strikes with implied volatilities larger
        than upper bound. The upper bound is computed as MaxOfMedianImpliedVolPercent
        multiplied by median implied volatility and divided by 100. The value is
        expressed in percentages.
        Mandatory if strikeRange object is used.
    min_of_median_implied_vol_percent : float, optional
        The value can be used to exclude strikes with implied volatilities less than
        lower bound. The lower bound is computed as MinOfMedianImpliedVolPercent
        multiplied by median implied volatility and divided by 100.
        The value is expressed in percentages.
    """

    def __init__(
        self,
        max_of_median_implied_vol_percent: "OptFloat" = None,
        min_of_median_implied_vol_percent: "OptFloat" = None,
    ):
        super().__init__()
        self.max_of_median_implied_vol_percent = max_of_median_implied_vol_percent
        self.min_of_median_implied_vol_percent = min_of_median_implied_vol_percent

    @property
    def max_of_median_implied_vol_percent(self):
        """
        Remove strikes whose implied vol is more than MaxOfMedianImpliedVolPercent x Median implied Vol.
        :return: float
        """
        return self._get_parameter("maxOfMedianImpliedVolPercent")

    @max_of_median_implied_vol_percent.setter
    def max_of_median_implied_vol_percent(self, value):
        self._set_parameter("maxOfMedianImpliedVolPercent", value)

    @property
    def min_of_median_implied_vol_percent(self):
        """
        Remove strikes whose implied vol is less than MinOfMedianImpliedVolPercent x Median implied Vol.
        :return: float
        """
        return self._get_parameter("minOfMedianImpliedVolPercent")

    @min_of_median_implied_vol_percent.setter
    def min_of_median_implied_vol_percent(self, value):
        self._set_parameter("minOfMedianImpliedVolPercent", value)
