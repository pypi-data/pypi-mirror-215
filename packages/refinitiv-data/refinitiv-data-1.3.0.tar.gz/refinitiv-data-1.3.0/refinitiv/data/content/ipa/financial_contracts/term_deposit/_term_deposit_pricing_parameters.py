from typing import Optional, Union

from ..._enums import PriceSide
from ..._object_definition import ObjectDefinition
from ....._types import OptDateTime


class PricingParameters(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    price_side : PriceSide or str, optional
        Price Side to consider when retrieving Market Data.
    market_data_date : str or date or datetime or timedelta, optional
        The market data date for pricing.
        By default, the market_data_date date is the valuation_date or Today.
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). It is set for the fields ending with 'xxxinreportccy'. Optional. The
        default value is the notional currency.
    valuation_date : str or date or datetime or timedelta, optional
        The valuation date for pricing. If not set the valuation date is equal to
        market_data_date or Today. For assets that contains a settlementConvention, the
        default valuation date  is equal to the settlementdate of the Asset that is
        usually the TradeDate+SettlementConvention.

    Examples
    --------
    >>> import refinitiv.data.content.ipa.financial_contracts as rdf
    >>> rdf.term_deposit.PricingParameters(valuation_date="2020-04-24")
    """

    _income_tax_percent = None

    def __init__(
        self,
        price_side: Union[PriceSide, str] = None,
        income_tax_percent: Optional[float] = None,
        market_data_date: "OptDateTime" = None,
        report_ccy: Optional[str] = None,
        valuation_date: "OptDateTime" = None,
    ):
        super().__init__()
        self.price_side = price_side
        self.income_tax_percent = income_tax_percent
        self.market_data_date = market_data_date
        self.report_ccy = report_ccy
        self.valuation_date = valuation_date

    @property
    def price_side(self):
        """
        Price Side to consider when retrieving Market Data.
        :return: enum PriceSide
        """
        return self._get_enum_parameter(PriceSide, "priceSide")

    @price_side.setter
    def price_side(self, value):
        self._set_enum_parameter(PriceSide, "priceSide", value)

    @property
    def income_tax_percent(self):
        return self._income_tax_percent

    @income_tax_percent.setter
    def income_tax_percent(self, value):
        self._income_tax_percent = value

    @property
    def market_data_date(self):
        """
        The market data date for pricing.
        By default, the marketDataDate date is the ValuationDate or Today.
        :return: str
        """
        return self._get_parameter("marketDataDate")

    @market_data_date.setter
    def market_data_date(self, value):
        self._set_datetime_parameter("marketDataDate", value)

    @property
    def report_ccy(self):
        """
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
        :return: str
        """
        return self._get_parameter("reportCcy")

    @report_ccy.setter
    def report_ccy(self, value):
        self._set_parameter("reportCcy", value)

    @property
    def valuation_date(self):
        """
        The date at which the instrument is valued. the value is expressed in iso 8601
        format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). by default,
        marketdatadate is used. if marketdatadate is not specified, the default value is
        today.
        :return: str
        """
        return self._get_parameter("valuationDate")

    @valuation_date.setter
    def valuation_date(self, value):
        self._set_datetime_parameter("valuationDate", value)
