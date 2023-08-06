from typing import TYPE_CHECKING, Any, Union

from ._shift_scenario import ShiftScenario
from ._forward_curve_definition import ForwardCurveDefinition
from ._swap_zc_curve_definition import SwapZcCurveDefinition
from ._swap_zc_curve_parameters import SwapZcCurveParameters
from .._object_definition import ObjectDefinition
from ...._tools import ArgsParser

if TYPE_CHECKING:
    from ...._types import OptStr
    from ._forward_curve_types import (
        ShiftScenarios,
        CurveDefinition,
        CurveParameters,
        ForwardCurveDefinitions,
    )


def parse_objects(param: object) -> Union[list, Any]:
    if not param:
        return param

    if not isinstance(param, list):
        param = [param]

    return param


object_arg_parser = ArgsParser(parse_objects)


class ForwardCurveRequestItem(ObjectDefinition):
    """
    Parameters
    ----------
    curve_definition : SwapZcCurveDefinition, optional

    curve_parameters : SwapZcCurveParameters, optional

    forward_curve_definitions : list of ForwardCurveDefinition, optional

    curve_tag : str, optionalx

    shift_scenarios : list of ShiftScenario, optional

    """

    def __init__(
        self,
        curve_definition: "CurveDefinition" = None,
        forward_curve_definitions: "ForwardCurveDefinitions" = None,
        curve_parameters: "CurveParameters" = None,
        curve_tag: "OptStr" = None,
        shift_scenarios: "ShiftScenarios" = None,
    ) -> None:
        super().__init__()
        self.curve_definition = curve_definition
        self.curve_parameters = curve_parameters
        self.forward_curve_definitions = object_arg_parser.parse(forward_curve_definitions)
        self.curve_tag = curve_tag
        self.shift_scenarios = object_arg_parser.parse(shift_scenarios)

    @property
    def curve_definition(self):
        """
        :return: object SwapZcCurveDefinition
        """
        return self._get_object_parameter(SwapZcCurveDefinition, "curveDefinition")

    @curve_definition.setter
    def curve_definition(self, value):
        self._set_object_parameter(SwapZcCurveDefinition, "curveDefinition", value)

    @property
    def curve_parameters(self):
        """
        :return: object SwapZcCurveParameters
        """
        return self._get_object_parameter(SwapZcCurveParameters, "curveParameters")

    @curve_parameters.setter
    def curve_parameters(self, value):
        self._set_object_parameter(SwapZcCurveParameters, "curveParameters", value)

    @property
    def forward_curve_definitions(self):
        """
        :return: list ForwardCurveDefinition
        """
        return self._get_list_parameter(ForwardCurveDefinition, "forwardCurveDefinitions")

    @forward_curve_definitions.setter
    def forward_curve_definitions(self, value):
        self._set_list_parameter(ForwardCurveDefinition, "forwardCurveDefinitions", value)

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
        :return: list ShiftScenario
        """
        return self._get_list_parameter(ShiftScenario, "shiftScenarios")

    @shift_scenarios.setter
    def shift_scenarios(self, value):
        self._set_list_parameter(ShiftScenario, "shiftScenarios", value)
