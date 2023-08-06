from typing import Optional

from ._models._par_rate_shift import ParRateShift
from .._object_definition import ObjectDefinition


class ShiftScenario(ObjectDefinition):
    """
    Parameters
    ----------
    par_rate_shift : ParRateShift, optional
        Scenario of par rates shift (shift applied to constituents).
    shift_tag : str, optional
        User defined string to identify the shift scenario tag. it can be used to link
        output curve to the shift scenario. only alphabetic, numeric and '- _.#=@'
        characters are supported. optional.
    zc_curve_shift : dict, optional
        Collection of shift parameters tenor. "all" selector supported as well.
    """

    def __init__(
        self,
        *,
        par_rate_shift: Optional[ParRateShift] = None,
        shift_tag: Optional[str] = None,
        zc_curve_shift: Optional[dict] = None,
    ) -> None:
        super().__init__()
        self.par_rate_shift = par_rate_shift
        self.shift_tag = shift_tag
        self.zc_curve_shift = zc_curve_shift

    @property
    def par_rate_shift(self):
        """
        Scenario of par rates shift (shift applied to constituents).
        :return: object ParRateShift
        """
        return self._get_object_parameter(ParRateShift, "parRateShift")

    @par_rate_shift.setter
    def par_rate_shift(self, value):
        self._set_object_parameter(ParRateShift, "parRateShift", value)

    @property
    def shift_tag(self):
        """
        User defined string to identify the shift scenario tag. it can be used to link
        output curve to the shift scenario. only alphabetic, numeric and '- _.#=@'
        characters are supported. optional.
        :return: str
        """
        return self._get_parameter("shiftTag")

    @shift_tag.setter
    def shift_tag(self, value):
        self._set_parameter("shiftTag", value)

    @property
    def zc_curve_shift(self):
        """
        Collection of shift parameters tenor. "all" selector supported as well.
        :return: dict
        """
        return self._get_parameter("zcCurveShift")

    @zc_curve_shift.setter
    def zc_curve_shift(self, value):
        self._set_parameter("zcCurveShift", value)
