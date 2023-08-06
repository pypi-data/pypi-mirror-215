from ._enums import UnderlyingType
from ._surface_request_item import SurfaceRequestItem
from ._swaption_calculation_params import SwaptionCalculationParams
from ._swaption_surface_definition import SwaptionSurfaceDefinition


class SwaptionSurfaceRequestItem(SurfaceRequestItem):
    # new name VolatilityCubeSurfaceRequestItem in version 1.0.130
    _instrument_type = None

    def __init__(
        self,
        instrument_type=None,
        surface_layout=None,
        surface_parameters=None,
        underlying_definition=None,
        surface_tag=None,
    ):
        super().__init__(
            surface_layout=surface_layout,
            surface_tag=surface_tag,
            underlying_type=UnderlyingType.SWAPTION,
        )
        self.instrument_type = instrument_type
        self.surface_parameters = surface_parameters
        self.underlying_definition = underlying_definition

    @property
    def surface_parameters(self):
        """
        :return: object SwaptionCalculationParams
        """
        return self._get_object_parameter(SwaptionCalculationParams, "surfaceParameters")

    @surface_parameters.setter
    def surface_parameters(self, value):
        self._set_object_parameter(SwaptionCalculationParams, "surfaceParameters", value)

    @property
    def underlying_definition(self):
        """
        :return: object SwaptionSurfaceDefinition
        """
        return self._get_object_parameter(SwaptionSurfaceDefinition, "underlyingDefinition")

    @underlying_definition.setter
    def underlying_definition(self, value):
        self._set_object_parameter(SwaptionSurfaceDefinition, "underlyingDefinition", value)

    @property
    def instrument_type(self):
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, value):
        self._instrument_type = value
