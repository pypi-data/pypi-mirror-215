# coding: utf8

from typing import Optional, Union

from ....._types import OptDateTime
from ._enums import (
    BuySell,
    CallPut,
    ExerciseStyle,
    UnderlyingType,
)
from .._instrument_definition import InstrumentDefinition


class OptionDefinition(InstrumentDefinition):
    """
    Parameters
    ----------
    instrument_tag : str, optional
        User defined string to identify the instrument.It can be used to link output
        results to the instrument definition. Only alphabetic, numeric and '- _.#=@'
        characters are supported. Optional.
    end_date : str or date or datetime or timedelta, optional
        Expiry date of the option.
    buy_sell : BuySell or str, optional
        The side of the deal.
    call_put : CallPut or str, optional
        Tells if the option is a call or a put.
    exercise_style : ExerciseStyle or str, optional
        The option style based on its exercise restrictions.
    underlying_type : UnderlyingType or str, optional
        Underlying type of the option.
    strike : float, optional
        strike of the option
    """

    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        buy_sell: Union[BuySell, str] = None,
        call_put: Union[CallPut, str] = None,
        exercise_style: Union[ExerciseStyle, str] = None,
        underlying_type: Union[UnderlyingType, str] = None,
        strike: Optional[float] = None,
        **kwargs,
    ) -> None:
        super().__init__(instrument_tag, **kwargs)
        self.instrument_tag = instrument_tag
        self.start_date = start_date
        self.end_date = end_date
        self.buy_sell = buy_sell
        self.call_put = call_put
        self.exercise_style = exercise_style
        self.underlying_type = underlying_type
        self.strike = strike

    def get_instrument_type(self):
        return "Option"

    @property
    def buy_sell(self):
        """
        The side of the deal. Possible values:
        - Buy
        - Sell
        :return: enum BuySell
        """
        return self._get_enum_parameter(BuySell, "buySell")

    @buy_sell.setter
    def buy_sell(self, value):
        self._set_enum_parameter(BuySell, "buySell", value)

    @property
    def call_put(self):
        """
        Tells if the option is a call or a put. Possible values:
        - Call
        - Put
        :return: enum CallPut
        """
        return self._get_enum_parameter(CallPut, "callPut")

    @call_put.setter
    def call_put(self, value):
        self._set_enum_parameter(CallPut, "callPut", value)

    @property
    def exercise_style(self):
        """
        EURO or AMER
        :return: enum ExerciseStyle
        """
        return self._get_enum_parameter(ExerciseStyle, "exerciseStyle")

    @exercise_style.setter
    def exercise_style(self, value):
        self._set_enum_parameter(ExerciseStyle, "exerciseStyle", value)

    @property
    def underlying_type(self):
        """
        Underlying type of the option. Possible values:
        - Eti
        - Fx
        :return: enum UnderlyingType
        """
        return self._get_enum_parameter(UnderlyingType, "underlyingType")

    @underlying_type.setter
    def underlying_type(self, value):
        self._set_enum_parameter(UnderlyingType, "underlyingType", value)

    @property
    def end_date(self):
        """
        Expiry date of the option
        :return: str
        """
        return self._get_parameter("endDate")

    @end_date.setter
    def end_date(self, value):
        self._set_datetime_parameter("endDate", value)

    @property
    def start_date(self):
        """
        Start date of the option
        :return: str
        """
        return self._get_parameter("startDate")

    @start_date.setter
    def start_date(self, value):
        self._set_datetime_parameter("startDate", value)

    @property
    def strike(self):
        """
        strike of the option
        :return: float
        """
        return self._get_parameter("strike")

    @strike.setter
    def strike(self, value):
        self._set_parameter("strike", value)
