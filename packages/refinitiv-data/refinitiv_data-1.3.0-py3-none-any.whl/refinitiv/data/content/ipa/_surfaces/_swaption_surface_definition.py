from typing import TYPE_CHECKING, Optional

from .._object_definition import ObjectDefinition
from ._enums import DiscountingType


if TYPE_CHECKING:
    from ...._types import OptStr


class SwaptionSurfaceDefinition(ObjectDefinition):
    # new name VolatilityCubeDefinition in version 1.0.130
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
        Underlying index name (e.g. 'euribor').
    index_tenor : str, optional
        Index tenor of the projected zero curve used to calculate swap rates. the
        default value is the index tenor associated with the underlying swap structure
        (for eur_ab6e, 6m).
    underlying_swap_structure : str, optional
        Underlying swap structure, eg: eur_ab6e
    """

    def __init__(
        self,
        *,
        instrument_code: "OptStr" = None,
        discounting_type: Optional[DiscountingType] = None,
        index_name: "OptStr" = None,
        index_tenor: "OptStr" = None,
        underlying_swap_structure: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.instrument_code = instrument_code
        self.index_name = index_name
        self.index_tenor = index_tenor
        self.discounting_type = discounting_type
        self.underlying_swap_structure = underlying_swap_structure

    @property
    def discounting_type(self):
        """
        The discounting type of the interest rate volatility model. the default value is
        selected based on 'instrumentcode'.
        :return: enum DiscountingType
        """
        return self._get_enum_parameter(DiscountingType, "discountingType")

    @discounting_type.setter
    def discounting_type(self, value):
        self._set_enum_parameter(DiscountingType, "discountingType", value)

    @property
    def index_name(self):
        """
        Underlying index name (e.g. 'euribor').
        :return: str
        """
        return self._get_parameter("indexName")

    @index_name.setter
    def index_name(self, value):
        self._set_parameter("indexName", value)

    @property
    def index_tenor(self):
        """
        Index tenor of the projected zero curve used to calculate swap rates. the
        default value is the index tenor associated with the underlying swap structure
        (for eur_ab6e, 6m).
        :return: str
        """
        return self._get_parameter("indexTenor")

    @index_tenor.setter
    def index_tenor(self, value):
        self._set_parameter("indexTenor", value)

    @property
    def instrument_code(self):
        """
        The currency of the interest rate volatility model.
        :return: str
        """
        return self._get_parameter("instrumentCode")

    @instrument_code.setter
    def instrument_code(self, value):
        self._set_parameter("instrumentCode", value)

    @property
    def underlying_swap_structure(self):
        """
        Underlying swap structure, eg: eur_ab6e
        :return: str
        """
        return self._get_parameter("underlyingSwapStructure")

    @underlying_swap_structure.setter
    def underlying_swap_structure(self, value):
        self._set_parameter("underlyingSwapStructure", value)
