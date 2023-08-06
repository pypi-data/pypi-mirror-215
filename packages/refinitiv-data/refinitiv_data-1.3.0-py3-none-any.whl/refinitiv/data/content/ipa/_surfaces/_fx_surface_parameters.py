from typing import Optional

from ...._types import OptDateTime
from .._object_definition import ObjectDefinition

from ._enums import FxVolatilityModel
from ._enums import FxSwapCalculationMethod
from ._enums import PriceSide
from ._enums import TimeStamp
from ._enums import Axis
from ._models import BidAskMid
from ._models import InterpolationWeight


class FxSurfaceParameters(ObjectDefinition):
    """
    This class property contains the properties that may be used to control the
    calculation. It mainly covers dates, market data assumptions (e.g. interpolation),
    and pricing model preferences. Some Parameters are common to all volatility surfaces
    contracts, while others are specific to a particular type of volatility.

    Parameters
    ----------
    atm_volatility_object : BidAskMid, optional

    butterfly10_d_object : BidAskMid, optional

    butterfly25_d_object : BidAskMid, optional

    domestic_deposit_rate_percent_object : BidAskMid, optional

    foreign_deposit_rate_percent_object : BidAskMid, optional

    forward_points_object : BidAskMid, optional

    fx_spot_object : BidAskMid, optional

    fx_swap_calculation_method : FxSwapCalculationMethod, optional
        The method used to calculate an outright price or deposit rates.
        The possible values are:
            FxSwapImpliedFromDeposit: implied FX swap points are computed from deposit
            rates,
            DepositCcy1ImpliedFromFxSwap: the currency 1 deposit rates are computed
            using swap points,
            DepositCcy2ImpliedFromFxSwap: the currency 2 deposit rates are computed
            using swap points.
    implied_volatility_object : BidAskMid, optional

    interpolation_weight : InterpolationWeight, optional

    price_side : PriceSide, optional
        Specifies whether bid, ask, mid or settle is used to build the surface. if not
        precised, default to mid.
    risk_reversal10_d_object : BidAskMid, optional

    risk_reversal25_d_object : BidAskMid, optional

    time_stamp : TimeStamp, optional
        Define how the timestamp is selected:
        - open: the opening value of the valuationdate or if not available the close of
          the previous day is used.
        - default: the latest snapshot is used when valuationdate is today, the close
          price when valuationdate is in the past.
    volatility_model : VolatilityModel, optional
        The quantitative model used to generate the volatility surface. this may depend
        on the asset class. for fx volatility surface, we currently support the svi
        model.
    x_axis : Axis, optional
        Specifies the unit for the x axis (e.g. date, tenor)
    y_axis : Axis, optional
        Specifies the unit for the y axis (e.g. strike, delta). this may depend on the
        asset class. for fx volatility surface, we support both delta and strike.
    calculation_date : str or date or datetime or timedelta, optional
        The date the volatility surface is generated.
    cutoff_time : str, optional
        The cutoff time
    cutoff_time_zone : str, optional
        The cutoff time zone
    """

    def __init__(
        self,
        atm_volatility_object: Optional[BidAskMid] = None,
        butterfly10_d_object: Optional[BidAskMid] = None,
        butterfly25_d_object: Optional[BidAskMid] = None,
        domestic_deposit_rate_percent_object: Optional[BidAskMid] = None,
        foreign_deposit_rate_percent_object: Optional[BidAskMid] = None,
        forward_points_object: Optional[BidAskMid] = None,
        fx_spot_object: Optional[BidAskMid] = None,
        fx_swap_calculation_method: Optional[FxSwapCalculationMethod] = None,
        implied_volatility_object: Optional[BidAskMid] = None,
        interpolation_weight: Optional[InterpolationWeight] = None,
        price_side: Optional[PriceSide] = None,
        risk_reversal10_d_object: Optional[BidAskMid] = None,
        risk_reversal25_d_object: Optional[BidAskMid] = None,
        time_stamp: Optional[TimeStamp] = None,
        volatility_model: Optional[FxVolatilityModel] = None,
        x_axis: Optional[Axis] = None,
        y_axis: Optional[Axis] = None,
        calculation_date: "OptDateTime" = None,
        cutoff_time: Optional[str] = None,
        cutoff_time_zone: Optional[str] = None,
    ):
        super().__init__()
        self.atm_volatility_object = atm_volatility_object
        self.butterfly10_d_object = butterfly10_d_object
        self.butterfly25_d_object = butterfly25_d_object
        self.domestic_deposit_rate_percent_object = domestic_deposit_rate_percent_object
        self.foreign_deposit_rate_percent_object = foreign_deposit_rate_percent_object
        self.forward_points_object = forward_points_object
        self.fx_spot_object = fx_spot_object
        self.fx_swap_calculation_method = fx_swap_calculation_method
        self.implied_volatility_object = implied_volatility_object
        self.interpolation_weight = interpolation_weight
        self.price_side = price_side
        self.risk_reversal10_d_object = risk_reversal10_d_object
        self.risk_reversal25_d_object = risk_reversal25_d_object
        self.time_stamp = time_stamp
        self.volatility_model = volatility_model
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.calculation_date = calculation_date
        self.cutoff_time = cutoff_time
        self.cutoff_time_zone = cutoff_time_zone

    @property
    def atm_volatility_object(self):
        """
        At the money volatility at Expiry
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "atmVolatilityObject")

    @atm_volatility_object.setter
    def atm_volatility_object(self, value):
        self._set_object_parameter(BidAskMid, "atmVolatilityObject", value)

    @property
    def butterfly10_d_object(self):
        """
        BF 10 Days at Expiry
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "butterfly10DObject")

    @butterfly10_d_object.setter
    def butterfly10_d_object(self, value):
        self._set_object_parameter(BidAskMid, "butterfly10DObject", value)

    @property
    def butterfly25_d_object(self):
        """
        BF 25 Days at Expiry
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "butterfly25DObject")

    @butterfly25_d_object.setter
    def butterfly25_d_object(self, value):
        self._set_object_parameter(BidAskMid, "butterfly25DObject", value)

    @property
    def domestic_deposit_rate_percent_object(self):
        """
        Domestic Deposit Rate at Expiry
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "domesticDepositRatePercentObject")

    @domestic_deposit_rate_percent_object.setter
    def domestic_deposit_rate_percent_object(self, value):
        self._set_object_parameter(BidAskMid, "domesticDepositRatePercentObject", value)

    @property
    def foreign_deposit_rate_percent_object(self):
        """
        Foreign Deposit Rate at Expiry
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "foreignDepositRatePercentObject")

    @foreign_deposit_rate_percent_object.setter
    def foreign_deposit_rate_percent_object(self, value):
        self._set_object_parameter(BidAskMid, "foreignDepositRatePercentObject", value)

    @property
    def forward_points_object(self):
        """
        Forward Points at Expiry
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "forwardPointsObject")

    @forward_points_object.setter
    def forward_points_object(self, value):
        self._set_object_parameter(BidAskMid, "forwardPointsObject", value)

    @property
    def fx_spot_object(self):
        """
        Spot Price
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "fxSpotObject")

    @fx_spot_object.setter
    def fx_spot_object(self, value):
        self._set_object_parameter(BidAskMid, "fxSpotObject", value)

    @property
    def fx_swap_calculation_method(self):
        """
        The method we chose to price outrights using or not implied deposits. Possible values are:

         FxSwap (compute outrights using swap points),

         DepositCcy1ImpliedFromFxSwap (compute currency1 deposits using swap points),

         DepositCcy2ImpliedFromFxSwap (compute currency2 deposits using swap points).

         Optional. Defaults to 'FxSwap'.
        :return: enum FxSwapCalculationMethod
        """
        return self._get_enum_parameter(FxSwapCalculationMethod, "fxSwapCalculationMethod")

    @fx_swap_calculation_method.setter
    def fx_swap_calculation_method(self, value):
        self._set_enum_parameter(FxSwapCalculationMethod, "fxSwapCalculationMethod", value)

    @property
    def implied_volatility_object(self):
        """
        Implied Volatility at Expiry
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "impliedVolatilityObject")

    @implied_volatility_object.setter
    def implied_volatility_object(self, value):
        self._set_object_parameter(BidAskMid, "impliedVolatilityObject", value)

    @property
    def interpolation_weight(self):
        """
        Vol Term Structure Interpolation
        :return: object InterpolationWeight
        """
        return self._get_object_parameter(InterpolationWeight, "interpolationWeight")

    @interpolation_weight.setter
    def interpolation_weight(self, value):
        self._set_object_parameter(InterpolationWeight, "interpolationWeight", value)

    @property
    def price_side(self):
        """
        Specifies whether bid, ask or mid is used to build the surface.
        :return: enum PriceSide
        """
        return self._get_enum_parameter(PriceSide, "priceSide")

    @price_side.setter
    def price_side(self, value):
        self._set_enum_parameter(PriceSide, "priceSide", value)

    @property
    def risk_reversal10_d_object(self):
        """
        RR 10 Days at Expiry
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "riskReversal10DObject")

    @risk_reversal10_d_object.setter
    def risk_reversal10_d_object(self, value):
        self._set_object_parameter(BidAskMid, "riskReversal10DObject", value)

    @property
    def risk_reversal25_d_object(self):
        """
        RR 25 Days at Expiry
        :return: object BidAskMid
        """
        return self._get_object_parameter(BidAskMid, "riskReversal25DObject")

    @risk_reversal25_d_object.setter
    def risk_reversal25_d_object(self, value):
        self._set_object_parameter(BidAskMid, "riskReversal25DObject", value)

    @property
    def time_stamp(self):
        """
        Define how the timestamp is selected:
        - Open: the opening value of the valuationDate or if not available the close of the previous day is used.
        - Default: the latest snapshot is used when valuationDate is today, the close price when valuationDate is in the past.
        :return: enum TimeStamp
        """
        return self._get_enum_parameter(TimeStamp, "timeStamp")

    @time_stamp.setter
    def time_stamp(self, value):
        self._set_enum_parameter(TimeStamp, "timeStamp", value)

    @property
    def volatility_model(self):
        """
        The quantitative model used to generate the volatility surface. This may depend on the asset class.
        For Fx Volatility Surface, we currently support the SVI model.
        :return: enum FxVolatilityModel
        """
        return self._get_enum_parameter(FxVolatilityModel, "volatilityModel")

    @volatility_model.setter
    def volatility_model(self, value):
        self._set_enum_parameter(FxVolatilityModel, "volatilityModel", value)

    @property
    def x_axis(self):
        """
        Specifies the unit for the x axis (e.g. Date, Tenor)
        :return: enum Axis
        """
        return self._get_enum_parameter(Axis, "xAxis")

    @x_axis.setter
    def x_axis(self, value):
        self._set_enum_parameter(Axis, "xAxis", value)

    @property
    def y_axis(self):
        """
        Specifies the unit for the y axis (e.g. Strike, Delta). This may depend on the asset class.
        For Fx Volatility Surface, we support both Delta and Strike.
        :return: enum Axis
        """
        return self._get_enum_parameter(Axis, "yAxis")

    @y_axis.setter
    def y_axis(self, value):
        self._set_enum_parameter(Axis, "yAxis", value)

    @property
    def calculation_date(self):
        """
        The date the volatility surface is generated.
        :return: str
        """
        return self._get_parameter("calculationDate")

    @calculation_date.setter
    def calculation_date(self, value):
        self._set_datetime_parameter("calculationDate", value)

    @property
    def cutoff_time(self):
        """
        The cutoff time
        :return: str
        """
        return self._get_parameter("cutoffTime")

    @cutoff_time.setter
    def cutoff_time(self, value):
        self._set_parameter("cutoffTime", value)

    @property
    def cutoff_time_zone(self):
        """
        The cutoff time zone
        :return: str
        """
        return self._get_parameter("cutoffTimeZone")

    @cutoff_time_zone.setter
    def cutoff_time_zone(self, value):
        self._set_parameter("cutoffTimeZone", value)
