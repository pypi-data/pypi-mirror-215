__all__ = ["MoneynessWeight"]

from typing import TYPE_CHECKING

from ..._object_definition import ObjectDefinition


if TYPE_CHECKING:
    from ....._types import OptFloat


class MoneynessWeight(ObjectDefinition):
    """
    MoneynessWeight for surface.

    Parameters
    ----------
    max_moneyness : float, optional
        The upper bound of the moneyness range of options to which the specified
        weight should be applied for surface construction. The value is expressed in
        percentages (call option moneyness = UnderlyingPrice / Strike * 100; put option
        moneyness = Strike / UnderlyingPrice * 100). The value of 100 corresponds to
        at-the-money option.
    min_moneyness : float, optional
        The lower bound of the moneyness range of options to which the specified weight
        should be applied for surface construction. The value is expressed in
        percentages (call option moneyness = UnderlyingPrice / Strike * 100;
        put option moneyness = Strike / UnderlyingPrice * 100). The value of 100
        corresponds to at-the-money option.
    weight : float, optional
        The weight which should be applied to the options in the specified range of the
        moneyness. The value is expressed in absolute numbers. The contribution of a
        specific option is computed by the dividing the weight of the option by the
        sum of weights of all constituent options.
    """

    def __init__(
        self,
        max_moneyness: "OptFloat" = None,
        min_moneyness: "OptFloat" = None,
        weight: "OptFloat" = None,
    ):
        super().__init__()
        self.max_moneyness = max_moneyness
        self.min_moneyness = min_moneyness
        self.weight = weight

    @property
    def max_moneyness(self):
        """
        :return: float
        """
        return self._get_parameter("maxMoneyness")

    @max_moneyness.setter
    def max_moneyness(self, value):
        self._set_parameter("maxMoneyness", value)

    @property
    def min_moneyness(self):
        """
        :return: float
        """
        return self._get_parameter("minMoneyness")

    @min_moneyness.setter
    def min_moneyness(self, value):
        self._set_parameter("minMoneyness", value)

    @property
    def weight(self):
        """
        :return: float
        """
        return self._get_parameter("weight")

    @weight.setter
    def weight(self, value):
        self._set_parameter("weight", value)
