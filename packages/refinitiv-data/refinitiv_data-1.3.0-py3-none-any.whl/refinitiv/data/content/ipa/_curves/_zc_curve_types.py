from typing import Iterable, Union, Optional

from ._shift_scenario import ShiftScenario
from ._enums import ZcCurvesOutputs
from ._zc_curve_definitions import ZcCurveDefinitions
from ._zc_curve_parameters import ZcCurveParameters
from ._models import (
    Step,
    Turn,
    Constituents,
)
from ..curves import zc_curves
from ...._types import Strings

Steps = Union[Iterable[Step]]
Turns = Union[Iterable[Turn]]
ShiftScenarios = Optional[Iterable[ShiftScenario]]
OptConstituents = Optional[Constituents]
CurveDefinition = Optional[ZcCurveDefinitions]
CurveParameters = Optional[ZcCurveParameters]
DefnDefns = Union[zc_curves.Definition, Iterable[zc_curves.Definition]]
Outputs = Union[Strings, Iterable[ZcCurvesOutputs]]
