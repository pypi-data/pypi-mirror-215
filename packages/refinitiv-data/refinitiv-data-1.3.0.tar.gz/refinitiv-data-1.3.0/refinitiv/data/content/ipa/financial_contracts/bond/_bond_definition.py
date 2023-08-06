from typing import Optional, Union

from ....._types import OptDateTime
from ..._enums import (
    DateRollingConvention,
    DayCountBasis,
    InterestType,
    StubRule,
    Frequency,
    AdjustInterestToPaymentDate,
    IndexCompoundingMethod,
    BusinessDayConvention,
    Direction,
    IndexAverageMethod,
)
from ..._models import AmortizationItem
from .._instrument_definition import InstrumentDefinition
from ..._enums import IndexObservationMethod


class BondInstrumentDefinition(InstrumentDefinition):
    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        instrument_code: Optional[str] = None,
        end_date: "OptDateTime" = None,
        direction: Union[Direction, str] = None,
        interest_type: Union[InterestType, str] = None,
        notional_ccy: Optional[str] = None,
        notional_amount: Optional[float] = None,
        fixed_rate_percent: Optional[float] = None,
        spread_bp: Optional[float] = None,
        interest_payment_frequency: Union[Frequency, str] = None,
        interest_calculation_method: Union[DayCountBasis, str] = None,
        accrued_calculation_method: Union[DayCountBasis, str] = None,
        payment_business_day_convention: Union[BusinessDayConvention, str] = None,
        payment_roll_convention: Union[DateRollingConvention, str] = None,
        index_reset_frequency: Union[Frequency, str] = None,
        index_fixing_lag: Optional[int] = None,
        first_regular_payment_date: "OptDateTime" = None,
        last_regular_payment_date: "OptDateTime" = None,
        amortization_schedule: Optional[AmortizationItem] = None,
        payment_business_days: Optional[str] = None,
        adjust_interest_to_payment_date: Union[AdjustInterestToPaymentDate, str] = None,
        index_compounding_method: Union[IndexCompoundingMethod, str] = None,
        interest_payment_delay: Optional[int] = None,
        stub_rule: Union[StubRule, str] = None,
        issue_date: "OptDateTime" = None,
        index_average_method: Union[IndexAverageMethod, str] = None,
        first_accrual_date: "OptDateTime" = None,
        floor_strike_percent: Optional[float] = None,
        index_fixing_ric: Optional[str] = None,
        is_perpetual: Optional[bool] = None,
        template: Optional[str] = None,
        index_observation_method: Union[IndexObservationMethod, str] = None,
        fixed_rate_percent_schedule: Optional[dict] = None,
        instrument_type: Optional[str] = "Bond",
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.instrument_code = instrument_code
        self.end_date = end_date
        self.direction = direction
        self.interest_type = interest_type
        self.notional_ccy = notional_ccy
        self.notional_amount = notional_amount
        self.fixed_rate_percent = fixed_rate_percent
        self.spread_bp = spread_bp
        self.interest_payment_frequency = interest_payment_frequency
        self.interest_calculation_method = interest_calculation_method
        self.accrued_calculation_method = accrued_calculation_method
        self.payment_business_day_convention = payment_business_day_convention
        self.payment_roll_convention = payment_roll_convention
        self.index_reset_frequency = index_reset_frequency
        self.index_fixing_lag = index_fixing_lag
        self.first_regular_payment_date = first_regular_payment_date
        self.last_regular_payment_date = last_regular_payment_date
        self.amortization_schedule = amortization_schedule
        self.payment_business_days = payment_business_days
        self.adjust_interest_to_payment_date = adjust_interest_to_payment_date
        self.index_compounding_method = index_compounding_method
        self.interest_payment_delay = interest_payment_delay
        self.stub_rule = stub_rule
        self.issue_date = issue_date
        self.index_average_method = index_average_method
        self.first_accrual_date = first_accrual_date
        self.floor_strike_percent = floor_strike_percent
        self.index_fixing_ric = index_fixing_ric
        self.is_perpetual = is_perpetual
        self.template = template
        self.index_observation_method = index_observation_method
        self.fixed_rate_percent_schedule = fixed_rate_percent_schedule
        self._instrument_type = instrument_type

    def get_instrument_type(self):
        return self._instrument_type

    @property
    def accrued_calculation_method(self):
        """
        The Day Count Basis method used to calculate the accrued interest payments.
        Optional. By default, the same value than InterestCalculationMethod is used.
        :return: enum DayCountBasis
        """
        return self._get_enum_parameter(DayCountBasis, "accruedCalculationMethod")

    @accrued_calculation_method.setter
    def accrued_calculation_method(self, value):
        self._set_enum_parameter(DayCountBasis, "accruedCalculationMethod", value)

    @property
    def adjust_interest_to_payment_date(self):
        """
        A flag that indicates if the coupon dates are adjusted to the payment dates.
        Optional. By default 'false' is used.
        :return: enum AdjustInterestToPaymentDate
        """
        return self._get_enum_parameter(AdjustInterestToPaymentDate, "adjustInterestToPaymentDate")

    @adjust_interest_to_payment_date.setter
    def adjust_interest_to_payment_date(self, value):
        self._set_enum_parameter(AdjustInterestToPaymentDate, "adjustInterestToPaymentDate", value)

    @property
    def amortization_schedule(self):
        """
        Definition of amortizations
        :return: list AmortizationItem
        """
        return self._get_list_parameter(AmortizationItem, "amortizationSchedule")

    @amortization_schedule.setter
    def amortization_schedule(self, value):
        self._set_list_parameter(AmortizationItem, "amortizationSchedule", value)

    @property
    def direction(self):
        """
        The direction of the leg. the possible values are:
        - 'Paid' (the cash flows of the leg are paid to the counterparty),
        - 'Received' (the cash flows of the leg are received from the counterparty).
          Optional for a single leg instrument (like a bond), in that case default value
          is Received. It is mandatory for a multi-instrument leg instrument (like Swap
          or CDS leg).
        :return: enum Direction
        """
        return self._get_enum_parameter(Direction, "direction")

    @direction.setter
    def direction(self, value):
        self._set_enum_parameter(Direction, "direction", value)

    @property
    def index_average_method(self):
        """
        :return: enum IndexAverageMethod
        """
        return self._get_enum_parameter(IndexAverageMethod, "indexAverageMethod")

    @index_average_method.setter
    def index_average_method(self, value):
        self._set_enum_parameter(IndexAverageMethod, "indexAverageMethod", value)

    @property
    def index_compounding_method(self):
        """
        A flag that defines how the coupon rate is calculated from the reset floating
        rates when the reset frequency is higher than the interest payment frequency
        (e.g. daily index reset with quarterly interest payment). The possible values
        are:
        - Compounded (uses the compounded average rate from multiple fixings),
        - Average (uses the arithmetic average rate from multiple fixings),
        - Constant (uses the last published rate among multiple fixings),
        - AdjustedCompounded (uses Chinese 7-day repo fixing),
        - MexicanCompounded (uses Mexican Bremse fixing). Optional. By default
          'Constant' is used.
        :return: enum IndexCompoundingMethod
        """
        return self._get_enum_parameter(IndexCompoundingMethod, "indexCompoundingMethod")

    @index_compounding_method.setter
    def index_compounding_method(self, value):
        self._set_enum_parameter(IndexCompoundingMethod, "indexCompoundingMethod", value)

    @property
    def index_reset_frequency(self):
        """
        The reset frequency in case the leg Type is Float. Optional. By default the
        IndexTenor is used.
        :return: enum Frequency
        """
        return self._get_enum_parameter(Frequency, "indexResetFrequency")

    @index_reset_frequency.setter
    def index_reset_frequency(self, value):
        self._set_enum_parameter(Frequency, "indexResetFrequency", value)

    @property
    def interest_calculation_method(self):
        """
        The Day Count Basis method used to calculate the coupon interest payments.
        Mandatory.
        :return: enum DayCountBasis
        """
        return self._get_enum_parameter(DayCountBasis, "interestCalculationMethod")

    @interest_calculation_method.setter
    def interest_calculation_method(self, value):
        self._set_enum_parameter(DayCountBasis, "interestCalculationMethod", value)

    @property
    def interest_payment_frequency(self):
        """
        The frequency of the interest payments. Optional if an instrument code/style
        have been defined : in that case, value comes from reference data. Otherwise, it
        is mandatory.
        :return: enum Frequency
        """
        return self._get_enum_parameter(Frequency, "interestPaymentFrequency")

    @interest_payment_frequency.setter
    def interest_payment_frequency(self, value):
        self._set_enum_parameter(Frequency, "interestPaymentFrequency", value)

    @property
    def interest_type(self):
        """
        A flag that indicates whether the leg is fixed or float. Possible values are:
        - 'Fixed' (the leg has a fixed coupon),
        - 'Float' (the leg has a floating rate index). Mandatory.
        :return: enum InterestType
        """
        return self._get_enum_parameter(InterestType, "interestType")

    @interest_type.setter
    def interest_type(self, value):
        self._set_enum_parameter(InterestType, "interestType", value)

    @property
    def payment_business_day_convention(self):
        """
        The method to adjust dates to a working day. The possible values are:
        - ModifiedFollowing (adjusts dates according to the Modified Following
          convention - next business day unless is it goes into the next month,
          preceeding is used in that  case),
        - NextBusinessDay (adjusts dates according to the Following convention - Next
          Business Day),
        - PreviousBusinessDay (adjusts dates  according to the Preceeding convention -
          Previous Business Day),
        - NoMoving (does not adjust dates),
        - BbswModifiedFollowing (adjusts dates  according to the BBSW Modified Following
          convention). Optional. In case an instrument code/style has been defined,
          value comes from bond reference data. Otherwise 'ModifiedFollowing' is used.
        :return: enum BusinessDayConvention
        """
        return self._get_enum_parameter(BusinessDayConvention, "paymentBusinessDayConvention")

    @payment_business_day_convention.setter
    def payment_business_day_convention(self, value):
        self._set_enum_parameter(BusinessDayConvention, "paymentBusinessDayConvention", value)

    @property
    def payment_roll_convention(self):
        """
        Method to adjust payment dates when they fall at the end of the month (28th of
        February, 30th, 31st). The possible values are:
        - Last (For setting the calculated date to the last working day),
        - Same (For setting the calculated date to the same day . In this latter case,
          the date may be moved according to the date moving convention if it is a
          non-working day),
        - Last28 (For setting the calculated date to the last working day. 28FEB being
          always considered as the last working day),
        - Same28 (For setting the calculated date to the same day .28FEB being always
          considered as the last working day). Optional. In case an instrument code has
          been defined, value comes from bond reference data. Otherwise, 'SameDay' is
          used.
        :return: enum DateRollingConvention
        """
        return self._get_enum_parameter(DateRollingConvention, "paymentRollConvention")

    @payment_roll_convention.setter
    def payment_roll_convention(self, value):
        self._set_enum_parameter(DateRollingConvention, "paymentRollConvention", value)

    @property
    def stub_rule(self):
        """
        The rule that defines whether coupon roll dates are aligned on the  maturity or
        the issue date.  The possible values are:
        - ShortFirstProRata (to create a short period between the start date and the
          first coupon date, and pay a smaller amount of interest for the short
          period.All coupon dates are calculated backward from the maturity date),
        - ShortFirstFull (to create a short period between the start date and the first
          coupon date, and pay a regular coupon on the first coupon date. All coupon
          dates are calculated backward from the maturity date),
        - LongFirstFull (to create a long period between the start date and the second
          coupon date, and pay a regular coupon on the second coupon date. All coupon
          dates are calculated backward from the maturity date),
        - ShortLastProRata (to create a short period between the last payment date and
          maturity, and pay a smaller amount of interest for the short period. All
          coupon dates are calculated forward from the start date). This property may
          also be used in conjunction with firstRegularPaymentDate and
          lastRegularPaymentDate; in that case the following values can be defined:
        - Issue (all dates are aligned on the issue date),
        - Maturity (all dates are aligned on the maturity date). Optional. By default
          'Maturity' is used.
        :return: enum StubRule
        """
        return self._get_enum_parameter(StubRule, "stubRule")

    @stub_rule.setter
    def stub_rule(self, value):
        self._set_enum_parameter(StubRule, "stubRule", value)

    @property
    def end_date(self):
        """
        Maturity date of the bond to override. Mandatory if instrument code has not been
        defined and is_perpetual flag has been set to false. In case an instrument code
        has been defined, value comes from bond reference data.
        :return: str
        """
        return self._get_parameter("endDate")

    @end_date.setter
    def end_date(self, value):
        self._set_datetime_parameter("endDate", value)

    @property
    def first_accrual_date(self):
        """
        Date at which bond starts accruing. Optional. In case an instrument code has
        been defined, value comes from bond reference data. Otherwise default value is
        the issue date of the bond.
        :return: str
        """
        return self._get_parameter("firstAccrualDate")

    @first_accrual_date.setter
    def first_accrual_date(self, value):
        self._set_datetime_parameter("firstAccrualDate", value)

    @property
    def first_regular_payment_date(self):
        """
        The first regular coupon payment date for leg with an odd first coupon.
        Optional.
        :return: str
        """
        return self._get_parameter("firstRegularPaymentDate")

    @first_regular_payment_date.setter
    def first_regular_payment_date(self, value):
        self._set_datetime_parameter("firstRegularPaymentDate", value)

    @property
    def fixed_rate_percent(self):
        """
        The fixed coupon rate in percentage. It is mandatory in case of a single leg
        instrument. Otherwise, in case of multi leg instrument, it can be computed as
        the Par rate.
        :return: float
        """
        return self._get_parameter("fixedRatePercent")

    @fixed_rate_percent.setter
    def fixed_rate_percent(self, value):
        self._set_parameter("fixedRatePercent", value)

    @property
    def floor_strike_percent(self):
        """
        The contractual strike rate of the floor. the value is expressed in percentages.
        if this parameter is set, the floor will apply to the leg with the same
        parameters set in the swapLegDefinition (e.g.maturity, frequency, index,
        discounting rule). no default value applies.
        :return: float
        """
        return self._get_parameter("floorStrikePercent")

    @floor_strike_percent.setter
    def floor_strike_percent(self, value):
        self._set_parameter("floorStrikePercent", value)

    @property
    def index_fixing_lag(self):
        """
        Defines the number of working days between the fixing date and the start of the
        coupon period ('InAdvance') or the end of the coupon period ('InArrears').
        Optional. By default 0 is used.
        :return: int
        """
        return self._get_parameter("indexFixingLag")

    @index_fixing_lag.setter
    def index_fixing_lag(self, value):
        self._set_parameter("indexFixingLag", value)

    @property
    def index_fixing_ric(self):
        """
        The RIC that carries the fixing value. This value overrides the RIC associated
        by default with the IndexName and IndexTenor. Optional.
        :return: str
        """
        return self._get_parameter("indexFixingRic")

    @index_fixing_ric.setter
    def index_fixing_ric(self, value):
        self._set_parameter("indexFixingRic", value)

    @property
    def instrument_code(self):
        """
        Code to define the bond instrument. It can be an ISIN, a RIC, a CUSIP or an
        AssetId .
        :return: str
        """
        return self._get_parameter("instrumentCode")

    @instrument_code.setter
    def instrument_code(self, value):
        self._set_parameter("instrumentCode", value)

    @property
    def instrument_tag(self):
        """
        User defined string to identify the instrument.It can be used to link output
        results to the instrument definition. Only alphabetic, numeric and '- _.#=@'
        characters are supported. Optional.
        :return: str
        """
        return self._get_parameter("instrumentTag")

    @instrument_tag.setter
    def instrument_tag(self, value):
        self._set_parameter("instrumentTag", value)

    @property
    def interest_payment_delay(self):
        """
        The number of working days between the end of coupon period and the actual
        interest payment date. Optional. By default no delay (0) is applied.
        :return: int
        """
        return self._get_parameter("interestPaymentDelay")

    @interest_payment_delay.setter
    def interest_payment_delay(self, value):
        self._set_parameter("interestPaymentDelay", value)

    @property
    def is_perpetual(self):
        """
        Flag the defines wether the bond is perpetual or not in case of user defined
        bond. Optional. In case an instrument code has been defined, value comes from
        bond reference data. In case of user defined bond, default value is 'false'.
        :return: bool
        """
        return self._get_parameter("isPerpetual")

    @is_perpetual.setter
    def is_perpetual(self, value):
        self._set_parameter("isPerpetual", value)

    @property
    def issue_date(self):
        """
        Date of issuance of the bond to override. Mandatory if instrument code has not
        been defined. In case an instrument code has been defined, value comes from bond
        reference data.
        :return: str
        """
        return self._get_parameter("issueDate")

    @issue_date.setter
    def issue_date(self, value):
        self._set_datetime_parameter("issueDate", value)

    @property
    def last_regular_payment_date(self):
        """
        The last regular coupon payment date for leg with an odd last coupon. Optional.
        :return: str
        """
        return self._get_parameter("lastRegularPaymentDate")

    @last_regular_payment_date.setter
    def last_regular_payment_date(self, value):
        self._set_datetime_parameter("lastRegularPaymentDate", value)

    @property
    def notional_amount(self):
        """
        The notional amount of the leg at the period start date. Optional. By default
        1,000,000 is used.
        :return: float
        """
        return self._get_parameter("notionalAmount")

    @notional_amount.setter
    def notional_amount(self, value):
        self._set_parameter("notionalAmount", value)

    @property
    def notional_ccy(self):
        """
        The ISO code of the notional currency. Mandatory if instrument code or
        instrument style has not been defined. In case an instrument code/style has been
        defined, value may comes from the reference data.
        :return: str
        """
        return self._get_parameter("notionalCcy")

    @notional_ccy.setter
    def notional_ccy(self, value):
        self._set_parameter("notionalCcy", value)

    @property
    def payment_business_days(self):
        """
        A list of coma-separated calendar codes to adjust dates (e.g. 'EMU' or 'USA').
        Optional. By default the calendar associated to notional_ccy is used.
        :return: str
        """
        return self._get_parameter("paymentBusinessDays")

    @payment_business_days.setter
    def payment_business_days(self, value):
        self._set_parameter("paymentBusinessDays", value)

    @property
    def spread_bp(self):
        """
        The spread in basis point that is added to the floating rate index index value.
        Optional. By default 0 is used.
        :return: float
        """
        return self._get_parameter("spreadBp")

    @spread_bp.setter
    def spread_bp(self, value):
        self._set_parameter("spreadBp", value)

    @property
    def template(self):
        """
        A reference to a Adfin instrument contract or the Adfin detailed contract.
        Optional. Either instrument_code, template, or full definition must be provided.
        :return: str
        """
        return self._get_parameter("template")

    @template.setter
    def template(self, value):
        self._set_parameter("template", value)

    @property
    def index_observation_method(self):
        return self._get_enum_parameter(IndexObservationMethod, "indexObservationMethod")

    @index_observation_method.setter
    def index_observation_method(self, value):
        self._set_enum_parameter(IndexObservationMethod, "indexObservationMethod", value)

    @property
    def fixed_rate_percent_schedule(self):
        return self._get_parameter("fixedRatePercentSchedule")

    @fixed_rate_percent_schedule.setter
    def fixed_rate_percent_schedule(self, value):
        self._set_parameter("fixedRatePercentSchedule", value)

    @property
    def instrument_type(self):
        return self._instrument_type
