from typing import Optional, TYPE_CHECKING

from ._enums import MarketDataAccessDeniedFallback
from ._models import InterestRateCurveParameters, ValuationTime
from .._object_definition import ObjectDefinition

from ._enums import (
    DayCountBasis,
    InterpolationMode,
    CalendarAdjustment,
    PriceSide,
    CompoundingType,
    ExtrapolationMode,
)
from ._models import (
    ConvexityAdjustment,
    Step,
    Turn,
)
from ...._types import Strings, OptBool, OptStr, OptDateTime
from ...._tools import create_repr, try_copy_to_list

if TYPE_CHECKING:
    from ._forward_curve_types import Steps, Turns


class SwapZcCurveParameters(ObjectDefinition):
    """
    Parameters
    ----------
    interest_calculation_method : InterestCalculationMethod, optional
        Day count basis of the calculated zero coupon rates.
        Default value is: Dcb_Actual_Actual
    calendar_adjustment : CalendarAdjustment, optional
        Cash flow adjustment according to a calendar
        No:
        Null:
        Weekend: for cash flow pricing using the calendar
        WeekendCalendar: for cash flow pricing using the calendar defined
                         by the parameter 'calendars'.
    calendars : string, optional
        A list of one or more calendar codes used to define non-working days and to
        adjust coupon dates and values.
    compounding_type : CompoundingType, optional

    convexity_adjustment : ConvexityAdjustment, optional

    extrapolation_mode : ExtrapolationMode, optional
        None: no extrapolation
        Constant: constant extrapolation
        Linear: linear extrapolation
    interpolation_mode : InterpolationMode, optional
        Interpolation method used in swap zero curve bootstrap.
        Default value is: CubicSpline
        CubicDiscount: local cubic interpolation of discount factors
        CubicRate: local cubic interpolation of rates
        CubicSpline: a natural cubic spline
        Linear: linear interpolation
        Log: log linear interpolation
        ForwardMonotoneConvex
    price_side : SwapPriceSide, optional
        Defines which data is used for the rate surface computation.
        Default value is: Mid
    steps : Step, optional
        Use to calculate the swap rate surface discount curve, when OIS is selected as
        discount curve.
        The steps can specify overnight index stepped dates or/and rates.
    turns : Turn, optional
        Used to include end period rates/turns when calculating swap rate surfaces
    reference_tenor : str, optional
        Root tenor(s) for the xIbor dependencies
    use_convexity_adjustment : bool, optional
        false / true
        Default value is: true.
        It indicates if the system needs to retrieve the convexity adjustment
    use_multi_dimensional_solver : bool, optional
        false / true
        Default value is: true.
        Specifies the use of the multi-dimensional solver for yield curve bootstrapping.
        This solving method is required because the bootstrapping method sometimes
        creates a ZC curve which does not accurately reprice the input instruments used
        to build it.
        The multi-dimensional solver is recommended when cubic interpolation methods
        are used in building the curve
        (in other cases, performance might be inferior to the regular bootstrapping
        method).
         - true: to use multi-dimensional solver for yield curve bootstrapping
         - false: not to use multi-dimensional solver for yield curve bootstrapping
    use_steps : bool, optional
        false / true
        Default value is: false.
        It indicates if the system needs to retrieve the overnight index
        stepped dates or/and rates
    valuation_date : str or date, optional
        The valuation date
        Default value is the current date
    market_data_access_denied_fallback : MarketDataAccessDeniedFallback, optional
        If at leat one constituent access is denied:
            * returnerror: dont price the surface and return an error (default value)
            * ignoreconstituents: price the surface without the error market data
            * usedelayeddata: use delayed market data if possible
    pivot_curve_parameters : list of InterestRateCurveParameters, optional
        The list of parameters used to define the pivot curve which is used for
        evaluation of the adjusted zero coupon curve. for example, eur zero curve
        adjusted with gbp curve, using usd as a pivot.
    reference_curve_parameters : list of InterestRateCurveParameters, optional
        The list of parameters used to define the reference curve which is used for
        evaluation of the adjusted zero coupon curve. for example, eur zero curve is
        adjusted with gbp curve.
    valuation_time : ValuationTime, optional
        The time identified by offsets at which the zero coupon curve is generated.
    ignore_invalid_instrument : bool, optional
        Ignore invalid instrument to calculate the curve.
        If false and some instrument are invlide, the curve is not calculated
        and an error is returned.  the default value is 'True'.
    use_delayed_data_if_denied : bool, optional
        Use delayed ric to retrieve data when not permissioned on constituent ric. The
        default value is 'False'.
    valuation_date_time : str or date or datetime or timedelta, optional
        The date and time at which the zero coupon curve is generated.
        The value is expressed in iso 8601 format: yyyy-mm-ddt00:00:00z
        (e.g., '2021-01-01t14:00:00z' or '2021-01-01t14:00:00+02:00').
        Only one parameter of valuation_date and valuation_date_time must be specified.
    """

    _ignore_existing_definition = None

    def __init__(
        self,
        interest_calculation_method: Optional[DayCountBasis] = None,
        calendar_adjustment: Optional[CalendarAdjustment] = None,
        calendars: Strings = None,
        compounding_type: Optional[CompoundingType] = None,
        convexity_adjustment: Optional[ConvexityAdjustment] = None,
        extrapolation_mode: Optional[ExtrapolationMode] = None,
        interpolation_mode: Optional[InterpolationMode] = None,
        price_side: Optional[PriceSide] = None,
        steps: "Steps" = None,
        turns: "Turns" = None,
        ignore_existing_definition: OptBool = None,
        reference_tenor: OptStr = None,
        use_convexity_adjustment: OptBool = None,
        use_multi_dimensional_solver: OptBool = None,
        use_steps: OptBool = None,
        valuation_date: "OptDateTime" = None,
        market_data_access_denied_fallback: Optional[MarketDataAccessDeniedFallback] = None,
        pivot_curve_parameters: Optional[InterestRateCurveParameters] = None,
        reference_curve_parameters: Optional[InterestRateCurveParameters] = None,
        valuation_time: Optional[ValuationTime] = None,
        ignore_invalid_instrument: OptBool = None,
        use_delayed_data_if_denied: OptBool = None,
        valuation_date_time: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.interest_calculation_method = interest_calculation_method
        self.calendar_adjustment = calendar_adjustment
        self.calendars = try_copy_to_list(calendars)
        self.compounding_type = compounding_type
        self.convexity_adjustment = convexity_adjustment
        self.extrapolation_mode = extrapolation_mode
        self.interpolation_mode = interpolation_mode
        self.price_side = price_side
        self.steps = try_copy_to_list(steps)
        self.turns = try_copy_to_list(turns)
        self.ignore_existing_definition = ignore_existing_definition
        self.reference_tenor = reference_tenor
        self.use_convexity_adjustment = use_convexity_adjustment
        self.use_multi_dimensional_solver = use_multi_dimensional_solver
        self.use_steps = use_steps
        self.valuation_date = valuation_date
        self.market_data_access_denied_fallback = market_data_access_denied_fallback

        self.pivot_curve_parameters = try_copy_to_list(pivot_curve_parameters)

        self.reference_curve_parameters = try_copy_to_list(reference_curve_parameters)

        self.valuation_time = valuation_time
        self.ignore_invalid_instrument = ignore_invalid_instrument
        self.use_delayed_data_if_denied = use_delayed_data_if_denied
        self.valuation_date_time = valuation_date_time

    def __repr__(self):
        return create_repr(
            self,
            middle_path="curves.forward_curves",
            class_name=self.__class__.__name__,
        )

    @property
    def calendar_adjustment(self):
        """
        Cash flow adjustment according to a calendar
        No:
        Null:
        Weekend: for cash flow pricing using the calendar
        WeekendCalendar: for cash flow pricing using the calendar defined
                         by the parameter 'calendars'.
        :return: enum CalendarAdjustment
        """
        return self._get_enum_parameter(CalendarAdjustment, "calendarAdjustment")

    @calendar_adjustment.setter
    def calendar_adjustment(self, value):
        self._set_enum_parameter(CalendarAdjustment, "calendarAdjustment", value)

    @property
    def calendars(self):
        """
        A list of one or more calendar codes used to define non-working days and to
        adjust coupon dates and values.
        :return: list string
        """
        return self._get_list_parameter(str, "calendars")

    @calendars.setter
    def calendars(self, value):
        self._set_list_parameter(str, "calendars", value)

    @property
    def compounding_type(self):
        """
        :return: enum CompoundingType
        """
        return self._get_enum_parameter(CompoundingType, "compoundingType")

    @compounding_type.setter
    def compounding_type(self, value):
        self._set_enum_parameter(CompoundingType, "compoundingType", value)

    @property
    def convexity_adjustment(self):
        """
        :return: object ConvexityAdjustment
        """
        return self._get_object_parameter(ConvexityAdjustment, "convexityAdjustment")

    @convexity_adjustment.setter
    def convexity_adjustment(self, value):
        self._set_object_parameter(ConvexityAdjustment, "convexityAdjustment", value)

    @property
    def extrapolation_mode(self):
        """
        None: no extrapolation
        Constant: constant extrapolation
        Linear: linear extrapolation
        :return: enum ExtrapolationMode
        """
        return self._get_enum_parameter(ExtrapolationMode, "extrapolationMode")

    @extrapolation_mode.setter
    def extrapolation_mode(self, value):
        self._set_enum_parameter(ExtrapolationMode, "extrapolationMode", value)

    @property
    def interest_calculation_method(self):
        """
        Day count basis of the calculated zero coupon rates.
        Default value is: Dcb_Actual_Actual
        :return: enum DayCountBasis
        """
        return self._get_enum_parameter(DayCountBasis, "interestCalculationMethod")

    @interest_calculation_method.setter
    def interest_calculation_method(self, value):
        self._set_enum_parameter(DayCountBasis, "interestCalculationMethod", value)

    @property
    def interpolation_mode(self):
        """
        Interpolation method used in swap zero curve bootstrap.
        Default value is: CubicSpline

        CubicDiscount: local cubic interpolation of discount factors
        CubicRate: local cubic interpolation of rates
        CubicSpline: a natural cubic spline
        Linear: linear interpolation
        Log: log linear interpolation
        ForwardMonotoneConvex
        :return: enum InterpolationMode
        """
        return self._get_enum_parameter(InterpolationMode, "interpolationMode")

    @interpolation_mode.setter
    def interpolation_mode(self, value):
        self._set_enum_parameter(InterpolationMode, "interpolationMode", value)

    @property
    def price_side(self):
        """
        Defines which data is used for the rate surface computation.
        Default value is: Mid
        :return: enum PriceSide
        """
        return self._get_enum_parameter(PriceSide, "priceSide")

    @price_side.setter
    def price_side(self, value):
        self._set_enum_parameter(PriceSide, "priceSide", value)

    @property
    def steps(self):
        """
        Use to calculate the swap rate surface discount curve, when OIS is selected as
        discount curve.
        The steps can specify overnight index stepped dates or/and rates.
        :return: list Step
        """
        return self._get_list_parameter(Step, "steps")

    @steps.setter
    def steps(self, value):
        self._set_list_parameter(Step, "steps", value)

    @property
    def turns(self):
        """
        Used to include end period rates/turns when calculating swap rate surfaces
        :return: list Turn
        """
        return self._get_list_parameter(Turn, "turns")

    @turns.setter
    def turns(self, value):
        self._set_list_parameter(Turn, "turns", value)

    @property
    def ignore_existing_definition(self):
        return self._ignore_existing_definition

    @ignore_existing_definition.setter
    def ignore_existing_definition(self, value):
        self._ignore_existing_definition = value

    @property
    def reference_tenor(self):
        """
        Root tenor(s) for the xIbor dependencies
        :return: str
        """
        return self._get_parameter("referenceTenor")

    @reference_tenor.setter
    def reference_tenor(self, value):
        self._set_parameter("referenceTenor", value)

    @property
    def use_convexity_adjustment(self):
        """
        false / true
        Default value is: true.
        It indicates if the system needs to retrieve the convexity adjustment
        :return: bool
        """
        return self._get_parameter("useConvexityAdjustment")

    @use_convexity_adjustment.setter
    def use_convexity_adjustment(self, value):
        self._set_parameter("useConvexityAdjustment", value)

    @property
    def use_multi_dimensional_solver(self):
        """
        false / true
        Default value is: true.
        Specifies the use of the multi-dimensional solver for yield curve bootstrapping.
        This solving method is required because the bootstrapping method sometimes
        creates a ZC curve which does not accurately reprice the input instruments used
        to build it.
        The multi-dimensional solver is recommended when cubic interpolation methods
        are used in building the curve
        (in other cases, performance might be inferior to the regular bootstrapping
        method).
         - true: to use multi-dimensional solver for yield curve bootstrapping
         - false: not to use multi-dimensional solver for yield curve bootstrapping
        :return: bool
        """
        return self._get_parameter("useMultiDimensionalSolver")

    @use_multi_dimensional_solver.setter
    def use_multi_dimensional_solver(self, value):
        self._set_parameter("useMultiDimensionalSolver", value)

    @property
    def use_steps(self):
        """
        false / true
        Default value is: false.
        It indicates if the system needs to retrieve the overnight index
        stepped dates or/and rates
        :return: bool
        """
        return self._get_parameter("useSteps")

    @use_steps.setter
    def use_steps(self, value):
        self._set_parameter("useSteps", value)

    @property
    def valuation_date(self):
        """
        The valuation date
        Default value is the current date
        :return: str
        """
        return self._get_parameter("valuationDate")

    @valuation_date.setter
    def valuation_date(self, value):
        self._set_date_parameter("valuationDate", value)

    @property
    def market_data_access_denied_fallback(self):
        """
        If at leat one constituent access is denied:
            * returnerror: dont price the surface and return an error (default value)
            * ignoreconstituents: price the surface without the error market data
            * usedelayeddata: use delayed market data if possible
        :return: enum MarketDataAccessDeniedFallback
        """
        return self._get_enum_parameter(MarketDataAccessDeniedFallback, "marketDataAccessDeniedFallback")

    @market_data_access_denied_fallback.setter
    def market_data_access_denied_fallback(self, value):
        self._set_enum_parameter(MarketDataAccessDeniedFallback, "marketDataAccessDeniedFallback", value)

    @property
    def pivot_curve_parameters(self):
        """
        The list of parameters used to define the pivot curve which is used for
        evaluation of the adjusted zero coupon curve. for example, eur zero curve
        adjusted with gbp curve, using usd as a pivot.
        :return: list InterestRateCurveParameters
        """
        return self._get_list_parameter(InterestRateCurveParameters, "pivotCurveParameters")

    @pivot_curve_parameters.setter
    def pivot_curve_parameters(self, value):
        self._set_list_parameter(InterestRateCurveParameters, "pivotCurveParameters", value)

    @property
    def reference_curve_parameters(self):
        """
        The list of parameters used to define the reference curve which is used for
        evaluation of the adjusted zero coupon curve. for example, eur zero curve is
        adjusted with gbp curve.
        :return: object InterestRateCurveParameters
        """
        return self._get_list_parameter(InterestRateCurveParameters, "referenceCurveParameters")

    @reference_curve_parameters.setter
    def reference_curve_parameters(self, value):
        self._set_list_parameter(InterestRateCurveParameters, "referenceCurveParameters", value)

    @property
    def valuation_time(self):
        """
        The time identified by offsets at which the zero coupon curve is generated.
        :return: object ValuationTime
        """
        return self._get_object_parameter(ValuationTime, "valuationTime")

    @valuation_time.setter
    def valuation_time(self, value):
        self._set_object_parameter(ValuationTime, "valuationTime", value)

    @property
    def ignore_invalid_instrument(self):
        """
        Ignore invalid instrument to calculate the curve.  if false and some instrument
        are invlide, the curve is not calculated and an error is returned.  the default
        value is 'true'.
        :return: bool
        """
        return self._get_parameter("ignoreInvalidInstrument")

    @ignore_invalid_instrument.setter
    def ignore_invalid_instrument(self, value):
        self._set_parameter("ignoreInvalidInstrument", value)

    @property
    def use_delayed_data_if_denied(self):
        """
        Use delayed ric to retrieve data when not permissioned on constituent ric. the
        default value is 'false'.
        :return: bool
        """
        return self._get_parameter("useDelayedDataIfDenied")

    @use_delayed_data_if_denied.setter
    def use_delayed_data_if_denied(self, value):
        self._set_parameter("useDelayedDataIfDenied", value)

    @property
    def valuation_date_time(self):
        """
        The date and time at which the zero coupon curve is generated.
        The value is expressed in iso 8601 format: yyyy-mm-ddt00:00:00z
        (e.g., '2021-01-01t14:00:00z' or '2021-01-01t14:00:00+02:00').
        Only one parameter of valuation_date and valuation_date_time must be specified.
        :return: str
        """
        return self._get_parameter("valuationDateTime")

    @valuation_date_time.setter
    def valuation_date_time(self, value):
        self._set_datetime_parameter("valuationDateTime", value)
