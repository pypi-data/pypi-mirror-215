from typing import TYPE_CHECKING, Optional

from ._enums import VolatilityAdjustmentType
from ._enums import Axis
from ._enums import InputVolatilityType
from ._models import SurfaceFilters
from .._enums import PriceSide, TimeStamp
from .._object_definition import ObjectDefinition


if TYPE_CHECKING:
    from ...._types import OptStr, OptFloat, OptDateTime


class IIrVolModelPricingParameters(ObjectDefinition):
    # new name CapletsStrippingSurfaceParameters in version 1.0.130
    """
    This class property contains the properties that may be used to control the
    calculation. It mainly covers dates, market data assumptions (e.g. interpolation),
    and pricing model preferences. Some Parameters are common to all volatility surfaces
    contracts, while others are specific to a particular type of volatility.

    Parameters
    ----------
    input_volatility_type : InputVolatilityType, optional
        User can specify whether calibration is based on normal or lognorma vol. however
        it would be preferrable to let the service determine the most appropriate one
    volatility_adjustment_type : VolatilityAdjustmentType, optional
        Volatility adjustment method applied to caplets surface before stripping. the
        default value is 'constantcap'.
    x_axis : Axis, optional
        The enumerate that specifies the unit for the x axis.
    y_axis : Axis, optional
        The enumerate that specifies the unit for the y axis.
    z_axis : Axis, optional
        Specifies the unit for the z axis (e.g. strike, expiry, tenor). this applies to
        swaption sabr cube.
    market_data_date : DEPRECATED
        This attribute doesn't use anymore.
    shift_percent : float, optional
        Shift applied to calibrated strikes allowing negative rates. the value is
        expressed in percentages. the default value is selected based oninstrumentcode
    source : str, optional
        Requested volatility data contributor.
    stripping_shift_percent : float, optional
        Shift value applied to strikes allowing the stripped caplets surface to include
        volatility even when some strikes are negative. the value is expressed in
        percentages. the default value is '0.0'.
    valuation_date : str or date or datetime or timedelta, optional
        The date at which the instrument is valued. the value is expressed in iso 8601
        format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). by default,
        marketdatadate is used. if marketdatadate is not specified, the default value is
        today.
    filters : SurfaceFilters, optional
    price_side : PriceSide, optional
        Specifies whether bid, ask, mid or settle is used to build the surface. if not
        precised, default to mid.
    time_stamp : TimeStamp, optional
        Define how the timestamp is selected:
        - open: the opening value of the valuationdate or if not available the close of
          the previous day is used.
        - default: the latest snapshot is used when valuationdate is today, the close
          price when valuationdate is in the past.
    calculation_date : str or date or datetime or timedelta, optional
        The date the volatility surface is generated.
    """

    _market_data_date = None

    def __init__(
        self,
        input_volatility_type: Optional[InputVolatilityType] = None,
        volatility_adjustment_type: Optional[VolatilityAdjustmentType] = None,
        x_axis: Optional[Axis] = None,
        y_axis: Optional[Axis] = None,
        z_axis: Optional[Axis] = None,
        market_data_date=None,
        shift_percent: "OptFloat" = None,
        source: "OptStr" = None,
        stripping_shift_percent: "OptFloat" = None,
        valuation_date: "OptDateTime" = None,
        filters: Optional[SurfaceFilters] = None,
        price_side: Optional[PriceSide] = None,
        time_stamp: Optional[TimeStamp] = None,
        calculation_date: "OptDateTime" = None,
    ):
        super().__init__()
        self.input_volatility_type = input_volatility_type
        self.volatility_adjustment_type = volatility_adjustment_type
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.z_axis = z_axis
        self.market_data_date = market_data_date
        self.shift_percent = shift_percent
        self.source = source
        self.stripping_shift_percent = stripping_shift_percent
        self.valuation_date = valuation_date
        self.filters = filters
        self.price_side = price_side
        self.time_stamp = time_stamp
        self.calculation_date = calculation_date

    @property
    def input_volatility_type(self):
        """
        :return: enum InputVolatilityType
        """
        return self._get_enum_parameter(InputVolatilityType, "inputVolatilityType")

    @input_volatility_type.setter
    def input_volatility_type(self, value):
        self._set_enum_parameter(InputVolatilityType, "inputVolatilityType", value)

    @property
    def volatility_adjustment_type(self):
        """
        Volatility Adjustment method for stripping: ConstantCaplet, ConstantCap, ShiftedCap, NormalizedCap, NormalizedCaplet
        :return: enum VolatilityAdjustmentType
        """
        return self._get_enum_parameter(VolatilityAdjustmentType, "volatilityAdjustmentType")

    @volatility_adjustment_type.setter
    def volatility_adjustment_type(self, value):
        self._set_enum_parameter(VolatilityAdjustmentType, "volatilityAdjustmentType", value)

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
    def z_axis(self):
        """
        Specifies the unit for the z axis (e.g. Strike, Tenor, Expiries). This applies on Ir SABR Volatility Cube.
        :return: enum Axis
        """
        return self._get_enum_parameter(Axis, "zAxis")

    @z_axis.setter
    def z_axis(self, value):
        self._set_enum_parameter(Axis, "zAxis", value)

    @property
    def market_data_date(self):
        return self._market_data_date

    @market_data_date.setter
    def market_data_date(self, value):
        self._market_data_date = value

    @property
    def shift_percent(self):
        """
        Shift value to use in calibration(Strike/Forward). Default: 0.0
        :return: float
        """
        return self._get_parameter("shiftPercent")

    @shift_percent.setter
    def shift_percent(self, value):
        self._set_parameter("shiftPercent", value)

    @property
    def source(self):
        """
        Requested volatility data contributor.
        :return: str
        """
        return self._get_parameter("source")

    @source.setter
    def source(self, value):
        self._set_parameter("source", value)

    @property
    def stripping_shift_percent(self):
        """
        Shift value to use in caplets stripping(Strike/Forward). Default: 0.0
        :return: float
        """
        return self._get_parameter("strippingShiftPercent")

    @stripping_shift_percent.setter
    def stripping_shift_percent(self, value):
        self._set_parameter("strippingShiftPercent", value)

    @property
    def valuation_date(self):
        """
        :return: str
        """
        return self._get_parameter("valuationDate")

    @valuation_date.setter
    def valuation_date(self, value):
        self._set_datetime_parameter("valuationDate", value)

    @property
    def filters(self):
        """
        :return: object SurfaceFilters
        """
        return self._get_object_parameter(SurfaceFilters, "filters")

    @filters.setter
    def filters(self, value):
        self._set_object_parameter(SurfaceFilters, "filters", value)

    @property
    def price_side(self):
        """
        Specifies whether bid, ask, mid or settle is used to build the surface. if not
        precised, default to mid.
        :return: enum PriceSide
        """
        return self._get_enum_parameter(PriceSide, "priceSide")

    @price_side.setter
    def price_side(self, value):
        self._set_enum_parameter(PriceSide, "priceSide", value)

    @property
    def time_stamp(self):
        """
        Define how the timestamp is selected:
        - open: the opening value of the valuationdate or if not available the close of
          the previous day is used.
        - default: the latest snapshot is used when valuationdate is today, the close
          price when valuationdate is in the past.
        :return: enum TimeStamp
        """
        return self._get_enum_parameter(TimeStamp, "timeStamp")

    @time_stamp.setter
    def time_stamp(self, value):
        self._set_enum_parameter(TimeStamp, "timeStamp", value)

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
