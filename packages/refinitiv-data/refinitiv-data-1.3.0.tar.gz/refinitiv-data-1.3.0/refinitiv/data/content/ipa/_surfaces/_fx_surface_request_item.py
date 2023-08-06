from typing import Optional, TYPE_CHECKING

from ._surface_request_item import SurfaceRequestItem

from ._enums import UnderlyingType
from ._fx_statistics_parameters import FxStatisticsParameters
from ._fx_surface_parameters import FxSurfaceParameters as FxCalculationParams
from ._fx_surface_definition import FxVolatilitySurfaceDefinition as FxSurfaceDefinition


if TYPE_CHECKING:
    from ...._types import OptStr


class FxSurfaceRequestItem(SurfaceRequestItem):
    # new name FxVolatilitySurfaceRequestItem into version 1.0.130
    def __init__(
        self,
        surface_layout=None,
        surface_parameters: Optional[FxCalculationParams] = None,
        underlying_definition: Optional[FxSurfaceDefinition] = None,
        surface_tag: "OptStr" = None,
        surface_statistics_parameters: Optional[FxStatisticsParameters] = None,
    ):
        super().__init__(
            surface_layout=surface_layout,
            surface_tag=surface_tag,
            underlying_type=UnderlyingType.FX,
        )
        self.surface_parameters = surface_parameters
        self.underlying_definition = underlying_definition
        self.surface_statistics_parameters = surface_statistics_parameters

    @property
    def surface_parameters(self):
        """
        The section that contains the properties that define how the volatility surface is generated
        :return: object FxCalculationParams
        """
        return self._get_object_parameter(FxCalculationParams, "surfaceParameters")

    @surface_parameters.setter
    def surface_parameters(self, value):
        self._set_object_parameter(FxCalculationParams, "surfaceParameters", value)

    @property
    def underlying_definition(self):
        """
        The section that contains the properties that define the underlying instrument
        :return: object FxSurfaceDefinition
        """
        return self._get_object_parameter(FxSurfaceDefinition, "underlyingDefinition")

    @underlying_definition.setter
    def underlying_definition(self, value):
        self._set_object_parameter(FxSurfaceDefinition, "underlyingDefinition", value)

    @property
    def surface_statistics_parameters(self):
        """
        :return: object FxStatisticsParameters
        """
        return self._get_object_parameter(FxStatisticsParameters, "surfaceStatisticsParameters")

    @surface_statistics_parameters.setter
    def surface_statistics_parameters(self, value):
        self._set_object_parameter(FxStatisticsParameters, "surfaceStatisticsParameters", value)
