from typing import TYPE_CHECKING
from .._object_definition import ObjectDefinition


if TYPE_CHECKING:
    from ...._types import OptStr, OptFloat, OptInt


class FxStatisticsParameters(ObjectDefinition):
    """
    FxStatisticsParameters for surface.

    Parameters
    ----------
    high_delta : float, optional

    low_delta : float, optional

    model : str, optional

    nb_points : int, optional
    """

    def __init__(
        self,
        *,
        high_delta: "OptFloat" = None,
        low_delta: "OptFloat" = None,
        model: "OptStr" = None,
        nb_points: "OptInt" = None,
    ) -> None:
        super().__init__()
        self.high_delta = high_delta
        self.low_delta = low_delta
        self.model = model
        self.nb_points = nb_points

    @property
    def high_delta(self):
        """
        :return: float
        """
        return self._get_parameter("highDelta")

    @high_delta.setter
    def high_delta(self, value):
        self._set_parameter("highDelta", value)

    @property
    def low_delta(self):
        """
        :return: float
        """
        return self._get_parameter("lowDelta")

    @low_delta.setter
    def low_delta(self, value):
        self._set_parameter("lowDelta", value)

    @property
    def model(self):
        """
        :return: str
        """
        return self._get_parameter("model")

    @model.setter
    def model(self, value):
        self._set_parameter("model", value)

    @property
    def nb_points(self):
        """
        :return: int
        """
        return self._get_parameter("nbPoints")

    @nb_points.setter
    def nb_points(self, value):
        self._set_parameter("nbPoints", value)
