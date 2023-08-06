from typing import TYPE_CHECKING, Optional
from .._object_definition import ObjectDefinition
from ._enums import RiskType
from ._enums import AssetClass


if TYPE_CHECKING:
    from ...._types import OptStr


class ZcCurveDefinitionRequest(ObjectDefinition):
    def __init__(
        self,
        index_name: "OptStr" = None,
        main_constituent_asset_class: Optional[AssetClass] = None,
        risk_type: Optional[RiskType] = None,
        currency: "OptStr" = None,
        curve_tag: "OptStr" = None,
        id: "OptStr" = None,
        name: "OptStr" = None,
        source: "OptStr" = None,
        valuation_date: "OptStr" = None,
        market_data_location: "OptStr" = None,
    ):
        super().__init__()
        self.index_name = index_name
        self.main_constituent_asset_class = main_constituent_asset_class
        self.risk_type = risk_type
        self.currency = currency
        self.curve_tag = curve_tag
        self.id = id
        self.name = name
        self.source = source
        self.valuation_date = valuation_date
        self.market_data_location = market_data_location

    @property
    def main_constituent_asset_class(self):
        """
        :return: enum AssetClass
        """
        return self._get_enum_parameter(AssetClass, "mainConstituentAssetClass")

    @main_constituent_asset_class.setter
    def main_constituent_asset_class(self, value):
        self._set_enum_parameter(AssetClass, "mainConstituentAssetClass", value)

    @property
    def risk_type(self):
        """
        :return: enum RiskType
        """
        return self._get_enum_parameter(RiskType, "riskType")

    @risk_type.setter
    def risk_type(self, value):
        self._set_enum_parameter(RiskType, "riskType", value)

    @property
    def currency(self):
        """
        The currency code of the interest rate curve
        :return: str
        """
        return self._get_parameter("currency")

    @currency.setter
    def currency(self, value):
        self._set_parameter("currency", value)

    @property
    def curve_tag(self):
        """
        User defined string to identify the curve. It can be used to link output results to the curve definition. Only alphabetic,
        numeric and '- _.#=@' characters are supported. Optional.
        :return: str
        """
        return self._get_parameter("curveTag")

    @curve_tag.setter
    def curve_tag(self, value):
        self._set_parameter("curveTag", value)

    @property
    def id(self):
        """
        Id of the curve definition
        :return: str
        """
        return self._get_parameter("id")

    @id.setter
    def id(self, value):
        self._set_parameter("id", value)

    @property
    def index_name(self):
        """
        :return: str
        """
        return self._get_parameter("indexName")

    @index_name.setter
    def index_name(self, value):
        self._set_parameter("indexName", value)

    @property
    def name(self):
        """
        The name of the interest rate curve
        :return: str
        """
        return self._get_parameter("name")

    @name.setter
    def name(self, value):
        self._set_parameter("name", value)

    @property
    def source(self):
        """
        :return: str
        """
        return self._get_parameter("source")

    @source.setter
    def source(self, value):
        self._set_parameter("source", value)

    @property
    def valuation_date(self):
        """
        :return: str
        """
        return self._get_parameter("valuationDate")

    @valuation_date.setter
    def valuation_date(self, value):
        self._set_date_parameter("valuationDate", value)

    @property
    def market_data_location(self):
        """
        The identifier of the market place from which constituents come from. currently
        the following values are supported: 'onshore' and 'emea'. the list of values can
        be extended by a user when creating a curve.
        :return: str
        """
        return self._get_parameter("marketDataLocation")

    @market_data_location.setter
    def market_data_location(self, value):
        self._set_parameter("marketDataLocation", value)
