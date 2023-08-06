from typing import TYPE_CHECKING, Optional
from .._object_definition import ObjectDefinition
from ._enums import DiscountingType

if TYPE_CHECKING:
    from ...._types import OptStr


class IIrVolModelDefinition(ObjectDefinition):
    # new name CapletsStrippingDefinition version 1.0.130
    """
    The definition of the volatility surface.

    Parameters
    ----------
    instrument_code : str, optional
        The currency of the interest rate volatility model.
    discounting_type : DiscountingType, optional
        The discounting type of the interest rate volatility model. the default value is
        selected based on 'instrumentcode'.
    index_name : str, optional
        Underlying index name.
    reference_caplet_tenor : str, optional
        Reference caplet payment or index tenor. ex: 1m, 3m, 6m, 1y.
    """

    def __init__(
        self,
        instrument_code: "OptStr" = None,
        discounting_type: Optional[DiscountingType] = None,
        index_name: "OptStr" = None,
        reference_caplet_tenor: "OptStr" = None,
    ):
        super().__init__()
        self.instrument_code = instrument_code
        self.discounting_type = discounting_type
        self.index_name = index_name
        self.reference_caplet_tenor = reference_caplet_tenor

    @property
    def discounting_type(self):
        """
        the discounting type of the IR vol model: OisDiscounting, or BorDiscounting (default)
        :return: enum DiscountingType
        """
        return self._get_enum_parameter(DiscountingType, "discountingType")

    @discounting_type.setter
    def discounting_type(self, value):
        self._set_enum_parameter(DiscountingType, "discountingType", value)

    @property
    def instrument_code(self):
        """
        The currency of the stripped cap surface, vol cube, or interest rate vol model
        :return: str
        """
        return self._get_parameter("instrumentCode")

    @instrument_code.setter
    def instrument_code(self, value):
        self._set_parameter("instrumentCode", value)

    @property
    def reference_caplet_tenor(self):
        """
        Reference caplet payment or index tenor. ex: 1m, 3m, 6m, 1y.
        :return: str
        """
        return self._get_parameter("referenceCapletTenor")

    @reference_caplet_tenor.setter
    def reference_caplet_tenor(self, value):
        self._set_parameter("referenceCapletTenor", value)

    @property
    def index_name(self):
        """
        Underlying index name.
        :return: str
        """
        return self._get_parameter("indexName")

    @index_name.setter
    def index_name(self, value):
        self._set_parameter("indexName", value)
