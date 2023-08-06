__all__ = ["VolatilitySurfacePoint"]

from typing import TYPE_CHECKING

from ..._object_definition import ObjectDefinition


if TYPE_CHECKING:
    from ....._types import OptStr


class VolatilitySurfacePoint(ObjectDefinition):
    """
    VolatilitySurfacePoint for surface.

    Parameters
    ----------
    x : str, optional
        The coordinate of the volatility data point on the x-axis
    y : str, optional
        The coordinate of the volatility data point on the y-axis
    """

    def __init__(self, x: "OptStr" = None, y: "OptStr" = None):
        super().__init__()
        self.x = x
        self.y = y

    @property
    def x(self):
        """
        The coordinate of the volatility data point on the x-axis
        :return: str
        """
        return self._get_parameter("x")

    @x.setter
    def x(self, value):
        self._set_parameter("x", value)

    @property
    def y(self):
        """
        The coordinate of the volatility data point on the y-axis
        :return: str
        """
        return self._get_parameter("y")

    @y.setter
    def y(self, value):
        self._set_parameter("y", value)
