from typing import TYPE_CHECKING

from ._shift_scenario import ShiftScenario
from .._object_definition import ObjectDefinition
from ._zc_curve_parameters import ZcCurveParameters
from ._models import Constituents
from ._zc_curve_definitions import ZcCurveDefinitions
from ...._tools import try_copy_to_list

if TYPE_CHECKING:
    from ...._types import OptStr
    from ._zc_curve_types import (
        CurveDefinition,
        CurveParameters,
        OptConstituents,
        ShiftScenarios,
    )


class ZcCurveRequestItem(ObjectDefinition):
    """
    Parameters
    ----------
    constituents : Constituents, optional

    curve_definition : ZcCurveDefinitions, optional

    curve_parameters : ZcCurveParameters, optional

    curve_tag : str, optional

    shift_scenarios : ShiftScenario, optional

    """

    def __init__(
        self,
        constituents: "OptConstituents" = None,
        curve_definition: "CurveDefinition" = None,
        curve_parameters: "CurveParameters" = None,
        curve_tag: "OptStr" = None,
        shift_scenarios: "ShiftScenarios" = None,
    ) -> None:
        super().__init__()
        self.constituents = constituents
        self.curve_definition = curve_definition
        self.curve_parameters = curve_parameters
        self.curve_tag = curve_tag
        self.shift_scenarios = try_copy_to_list(shift_scenarios)

    @property
    def constituents(self):
        """
        :return: object Constituents
        """
        return self._get_object_parameter(Constituents, "constituents")

    @constituents.setter
    def constituents(self, value):
        self._set_object_parameter(Constituents, "constituents", value)

    @property
    def curve_definition(self):
        """
        :return: object ZcCurveDefinitions
        """
        return self._get_object_parameter(ZcCurveDefinitions, "curveDefinition")

    @curve_definition.setter
    def curve_definition(self, value):
        self._set_object_parameter(ZcCurveDefinitions, "curveDefinition", value)

    @property
    def curve_parameters(self):
        """
        :return: object ZcCurveParameters
        """
        return self._get_object_parameter(ZcCurveParameters, "curveParameters")

    @curve_parameters.setter
    def curve_parameters(self, value):
        self._set_object_parameter(ZcCurveParameters, "curveParameters", value)

    @property
    def curve_tag(self):
        """
        :return: str
        """
        return self._get_parameter("curveTag")

    @curve_tag.setter
    def curve_tag(self, value):
        self._set_parameter("curveTag", value)

    @property
    def shift_scenarios(self):
        """
        The list of attributes applied to the curve shift scenarios.
        :return: list ShiftScenario
        """
        return self._get_list_parameter(ShiftScenario, "shiftScenarios")

    @shift_scenarios.setter
    def shift_scenarios(self, value):
        self._set_list_parameter(ShiftScenario, "shiftScenarios", value)
