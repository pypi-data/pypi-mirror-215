__all__ = ["MaturityFilter"]

from typing import TYPE_CHECKING

from ..._object_definition import ObjectDefinition


if TYPE_CHECKING:
    from ....._types import OptStr, OptFloat


class MaturityFilter(ObjectDefinition):
    """
    MaturityFilter for surface.

    Parameters
    ----------
    max_maturity : str, optional
        The period code used to set the maximal maturity of options used to construct
        the surface (e.g., '1M', '1Y').
    min_maturity : str, optional
        The period code used to set the minimal maturity of options used to construct
        the surface (e.g., '1M', '1Y').
    min_of_median_nb_of_strikes_percent : float, optional
        The value is used to set the minimum number of strikes that should be available
        for maturities that are used to construct the surface. The minimum threshold
        is computed as MinOfMedianNbOfStrikesPercent multiplied by the median number
        of Strikes and divided by 100. The value is expressed in percentages.
    """

    def __init__(
        self,
        max_maturity: "OptStr" = None,
        min_maturity: "OptStr" = None,
        min_of_median_nb_of_strikes_percent: "OptFloat" = None,
    ):
        super().__init__()
        self.max_maturity = max_maturity
        self.min_maturity = min_maturity
        self.min_of_median_nb_of_strikes_percent = min_of_median_nb_of_strikes_percent

    @property
    def max_maturity(self):
        """
        Max Maturity to consider in the filtering. (expressed in tenor)
        :return: str
        """
        return self._get_parameter("maxMaturity")

    @max_maturity.setter
    def max_maturity(self, value):
        self._set_parameter("maxMaturity", value)

    @property
    def min_maturity(self):
        """
        Min Maturity to consider in the filtering. (expressed in tenor)
        Default value: 7D
        :return: str
        """
        return self._get_parameter("minMaturity")

    @min_maturity.setter
    def min_maturity(self, value):
        self._set_parameter("minMaturity", value)

    @property
    def min_of_median_nb_of_strikes_percent(self):
        """
        Remove maturities whose number of strikes is less than MinOfMedianNbOfStrikesPercent of the Median number of Strikes.
        :return: float
        """
        return self._get_parameter("minOfMedianNbOfStrikesPercent")

    @min_of_median_nb_of_strikes_percent.setter
    def min_of_median_nb_of_strikes_percent(self, value):
        self._set_parameter("minOfMedianNbOfStrikesPercent", value)
