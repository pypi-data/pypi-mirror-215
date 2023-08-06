from typing import Optional, TYPE_CHECKING

from .._object_definition import ObjectDefinition
from ._enums import (
    AssetClass,
    RiskType,
    ConstituentOverrideMode,
)


if TYPE_CHECKING:
    from ...._types import OptStr, OptBool


class ZcCurveDefinition(ObjectDefinition):
    """
    Parameters
    ----------
    index_name : str, optional

    main_constituent_asset_class : AssetClass, optional

    risk_type : RiskType, optional

    currency : str, optional
        The currency code of the interest rate curve
    discounting_tenor : str, optional
        Mono currency discounting tenor
    id : str, optional
        Id of the curve definition
    name : str, optional
        The name of the interest rate curve
    source : str, optional
    constituent_override_mode : ConstituentOverrideMode, optional
        The possible values are:
          * replacedefinition: replace the default constituents by the user
              constituents from the input request,
          * mergewithdefinition: merge the default constituents and the user
              constituents from the input request, the default value is 'replacedefinition'.
        If the ignore_existing_definition is true, the constituent_override_mode
        is set to 'replacedefinition'.
    ignore_existing_definition : bool, optional
        An indicator whether default definitions are used to get curve parameters and
        constituents.
        The possible values are:
            * True: default definitions are not used (definitions and constituents
            must be set in the request),
            * False: default definitions are used.
    is_non_deliverable : bool, optional
        An indicator whether the instrument is non-deliverable.
        The possible values are:
            * True: the instrument is non-deliverable,
            * False: the instrument is not non-deliverable.
        This parameter may be used to specify the use of crosscurrencydefinitions made
        of non-deliverable or deliverable instruments. When this parameters isn't
        specified, the default crosscurrencydefinitions is used. this definition with
        'isfallbackforfxcurvedefinition'=True is returned by the
        crosscurrencydefinitions curve search.
    market_data_location : str, optional
        The identifier of the market place from which constituents come from. currently
        the following values are supported: 'onshore' and 'emea'. the list of values can
        be extended by a user when creating a curve.
    """

    def __init__(
        self,
        index_name: "OptStr" = None,
        main_constituent_asset_class: Optional[AssetClass] = None,
        risk_type: Optional[RiskType] = None,
        currency: "OptStr" = None,
        discounting_tenor: "OptStr" = None,
        id: "OptStr" = None,
        name: "OptStr" = None,
        source: "OptStr" = None,
        constituent_override_mode: Optional[ConstituentOverrideMode] = None,
        ignore_existing_definition: "OptBool" = None,
        is_non_deliverable: "OptBool" = None,
        market_data_location: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.index_name = index_name
        self.main_constituent_asset_class = main_constituent_asset_class
        self.risk_type = risk_type
        self.currency = currency
        self.discounting_tenor = discounting_tenor
        self.id = id
        self.name = name
        self.source = source
        self.constituent_override_mode = constituent_override_mode
        self.ignore_existing_definition = ignore_existing_definition
        self.is_non_deliverable = is_non_deliverable
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
    def discounting_tenor(self):
        """
        Mono currency discounting tenor
        :return: str
        """
        return self._get_parameter("discountingTenor")

    @discounting_tenor.setter
    def discounting_tenor(self, value):
        self._set_parameter("discountingTenor", value)

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
    def constituent_override_mode(self):
        """
        A method to use the default constituents. the possible values are:
          * replacedefinition: replace the default constituents by the user
              constituents from the input request,
          * mergewithdefinition: merge the default constituents and the user
              constituents from the input request, the default value is 'replacedefinition'.
        If the ignore_existing_definition is true, the constituent_override_mode
        is set to 'replacedefinition'.
        :return: enum ConstituentOverrideMode
        """
        return self._get_enum_parameter(ConstituentOverrideMode, "constituentOverrideMode")

    @constituent_override_mode.setter
    def constituent_override_mode(self, value):
        self._set_enum_parameter(ConstituentOverrideMode, "constituentOverrideMode", value)

    @property
    def ignore_existing_definition(self):
        """
        An indicator whether default definitions are used to get curve parameters and
        constituents.
        The possible values are:
            * True: default definitions are not used (definitions and constituents
            must be set in the request),
            * False: default definitions are used.
        :return: bool
        """
        return self._get_parameter("ignoreExistingDefinition")

    @ignore_existing_definition.setter
    def ignore_existing_definition(self, value):
        self._set_parameter("ignoreExistingDefinition", value)

    @property
    def is_non_deliverable(self):
        """
        An indicator whether the instrument is non-deliverable.
        The possible values are:
            * True: the instrument is non-deliverable,
            * False: the instrument is not non-deliverable.
        This parameter may be used to specify the use of crosscurrencydefinitions made
        of non-deliverable or deliverable instruments. When this parameters isn't
        specified, the default crosscurrencydefinitions is used. this definition with
        'isfallbackforfxcurvedefinition'=True is returned by the
        crosscurrencydefinitions curve search.
        :return: bool
        """
        return self._get_parameter("isNonDeliverable")

    @is_non_deliverable.setter
    def is_non_deliverable(self, value):
        self._set_parameter("isNonDeliverable", value)

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
