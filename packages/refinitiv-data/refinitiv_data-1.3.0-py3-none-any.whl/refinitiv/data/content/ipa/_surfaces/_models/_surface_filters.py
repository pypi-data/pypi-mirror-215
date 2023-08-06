__all__ = ["SurfaceFilters"]

from typing import Optional, TYPE_CHECKING

from ..._object_definition import ObjectDefinition

from ._maturity_filter import MaturityFilter
from ._strike_filter_range import StrikeFilterRange


if TYPE_CHECKING:
    from ....._types import OptBool, OptInt, OptFloat


class SurfaceFilters(ObjectDefinition):
    """
    Filter object for surface.

    Parameters
    ----------
    maturity_filter_range : MaturityFilter, optional
        The object allows to specify the range of expiry periods of options that are
        used to construct the surface.
    strike_range : StrikeFilterRange, optional
        The range allows to exclude strike levels that have implied volatilities which
        exceed upper bound or below lower bound.
    strike_range_percent : DEPRECATED
        This attribute doesn't use anymore.
    atm_tolerance_interval_percent : float, optional
        Filter on the atm tolerance interval percent
    ensure_prices_monotonicity : bool, optional
        Filter on the monotonicity of price options.
    max_of_median_bid_ask_spread : float, optional
        Spread mutltiplier to filter the options with the same expiry
    max_staleness_days : int, optional
        Max staleness past days to use for building the surface
    use_only_calls : bool, optional
        Select only teh calls to build the surface
    use_only_puts : bool, optional
        Select only the puts to build the surface
    use_weekly_options : bool, optional
        Filter on the weekly options.
    include_min_tick_prices : bool, optional
        Take into account the minimum tick prices to build the surface
    """

    _strike_range_percent = None

    def __init__(
        self,
        maturity_filter_range: Optional[MaturityFilter] = None,
        strike_range: Optional[StrikeFilterRange] = None,
        strike_range_percent=None,
        atm_tolerance_interval_percent: "OptFloat" = None,
        ensure_prices_monotonicity: "OptBool" = None,
        max_of_median_bid_ask_spread: "OptFloat" = None,
        max_staleness_days: "OptInt" = None,
        use_only_calls: "OptBool" = None,
        use_only_puts: "OptBool" = None,
        use_weekly_options: "OptBool" = None,
        include_min_tick_prices: "OptBool" = None,
    ):
        super().__init__()
        self.maturity_filter_range = maturity_filter_range
        self.strike_range = strike_range
        self.strike_range_percent = strike_range_percent
        self.atm_tolerance_interval_percent = atm_tolerance_interval_percent
        self.ensure_prices_monotonicity = ensure_prices_monotonicity
        self.max_of_median_bid_ask_spread = max_of_median_bid_ask_spread
        self.max_staleness_days = max_staleness_days
        self.use_only_calls = use_only_calls
        self.use_only_puts = use_only_puts
        self.use_weekly_options = use_weekly_options
        self.include_min_tick_prices = include_min_tick_prices

    @property
    def maturity_filter_range(self):
        """
        Define the MaturityFilterRange
        :return: object MaturityFilter
        """
        return self._get_object_parameter(MaturityFilter, "maturityFilterRange")

    @maturity_filter_range.setter
    def maturity_filter_range(self, value):
        self._set_object_parameter(MaturityFilter, "maturityFilterRange", value)

    @property
    def strike_range(self):
        """
        Define the StrikeFilterRange
        :return: object StrikeFilterRange
        """
        return self._get_object_parameter(StrikeFilterRange, "strikeRange")

    @strike_range.setter
    def strike_range(self, value):
        self._set_object_parameter(StrikeFilterRange, "strikeRange", value)

    @property
    def strike_range_percent(self):
        """
        [DEPRECATED]
        """
        return self._strike_range_percent

    @strike_range_percent.setter
    def strike_range_percent(self, value):
        self._strike_range_percent = value

    @property
    def atm_tolerance_interval_percent(self):
        """
        Filter on the ATM tolerance interval percent
        :return: float
        """
        return self._get_parameter("atmToleranceIntervalPercent")

    @atm_tolerance_interval_percent.setter
    def atm_tolerance_interval_percent(self, value):
        self._set_parameter("atmToleranceIntervalPercent", value)

    @property
    def ensure_prices_monotonicity(self):
        """
        Filter on the monotonicity of price options.
        :return: bool
        """
        return self._get_parameter("ensurePricesMonotonicity")

    @ensure_prices_monotonicity.setter
    def ensure_prices_monotonicity(self, value):
        self._set_parameter("ensurePricesMonotonicity", value)

    @property
    def max_of_median_bid_ask_spread(self):
        """
        Spread mutltiplier to filter the options with the same expiry
        :return: float
        """
        return self._get_parameter("maxOfMedianBidAskSpread")

    @max_of_median_bid_ask_spread.setter
    def max_of_median_bid_ask_spread(self, value):
        self._set_parameter("maxOfMedianBidAskSpread", value)

    @property
    def max_staleness_days(self):
        """
        Max Staleness past days to use for building the surface
        :return: int
        """
        return self._get_parameter("maxStalenessDays")

    @max_staleness_days.setter
    def max_staleness_days(self, value):
        self._set_parameter("maxStalenessDays", value)

    @property
    def use_only_calls(self):
        """
        SElect only teh calls to build the surface
        :return: bool
        """
        return self._get_parameter("useOnlyCalls")

    @use_only_calls.setter
    def use_only_calls(self, value):
        self._set_parameter("useOnlyCalls", value)

    @property
    def use_only_puts(self):
        """
        Select only the puts to build the surface
        :return: bool
        """
        return self._get_parameter("useOnlyPuts")

    @use_only_puts.setter
    def use_only_puts(self, value):
        self._set_parameter("useOnlyPuts", value)

    @property
    def use_weekly_options(self):
        """
        Filter on the weekly options.
        :return: bool
        """
        return self._get_parameter("useWeeklyOptions")

    @use_weekly_options.setter
    def use_weekly_options(self, value):
        self._set_parameter("useWeeklyOptions", value)

    @property
    def include_min_tick_prices(self):
        """
        Take into account the minimum tick prices to build the surface
        :return: bool
        """
        return self._get_parameter("includeMinTickPrices")

    @include_min_tick_prices.setter
    def include_min_tick_prices(self, value):
        self._set_parameter("includeMinTickPrices", value)
