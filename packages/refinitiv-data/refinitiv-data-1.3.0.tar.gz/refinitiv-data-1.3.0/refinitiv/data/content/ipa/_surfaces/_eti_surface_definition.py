from typing import TYPE_CHECKING
from .._object_definition import ObjectDefinition

if TYPE_CHECKING:
    from ...._types import OptStr, OptBool


class EtiSurfaceDefinition(ObjectDefinition):
    """
    The definition of the volatility surface.

    Parameters
    ----------
    instrument_code : str, optional
        The code (ric for equities and indices and ricroot for futures.) that represents
        the instrument. the format for equities and indices is xxx@ric (example:
        vod.l@ric) the format for futures is xx@ricroot (example: cl@ricroot)
    clean_instrument_code : str, optional
    exchange : str, optional
        Specifies the exchange to be used to retrieve the underlying data.
    is_future_underlying : bool, optional
    is_lme_future_underlying : bool, optional
    """

    def __init__(
        self,
        instrument_code: "OptStr" = None,
        clean_instrument_code: "OptStr" = None,
        exchange: "OptStr" = None,
        is_future_underlying: "OptBool" = None,
        is_lme_future_underlying: "OptBool" = None,
    ):
        super().__init__()
        self.instrument_code = instrument_code
        self.clean_instrument_code = clean_instrument_code
        self.exchange = exchange
        self.is_future_underlying = is_future_underlying
        self.is_lme_future_underlying = is_lme_future_underlying

    @property
    def clean_instrument_code(self):
        """
        :return: str
        """
        return self._get_parameter("cleanInstrumentCode")

    @clean_instrument_code.setter
    def clean_instrument_code(self, value):
        self._set_parameter("cleanInstrumentCode", value)

    @property
    def exchange(self):
        """
        Specifies the exchange to be used to retrieve the underlying data.
        :return: str
        """
        return self._get_parameter("exchange")

    @exchange.setter
    def exchange(self, value):
        self._set_parameter("exchange", value)

    @property
    def instrument_code(self):
        """
        The code (RIC for equities and indices and RICROOT for Futures.) that represents the instrument.
        The format for equities and indices is xxx@RIC (Example: VOD.L@RIC)
        The format for Futures is xx@RICROOT (Example: CL@RICROOT)
        :return: str
        """
        return self._get_parameter("instrumentCode")

    @instrument_code.setter
    def instrument_code(self, value):
        self._set_parameter("instrumentCode", value)

    @property
    def is_future_underlying(self):
        """
        :return: bool
        """
        return self._get_parameter("isFutureUnderlying")

    @is_future_underlying.setter
    def is_future_underlying(self, value):
        self._set_parameter("isFutureUnderlying", value)

    @property
    def is_lme_future_underlying(self):
        """
        :return: bool
        """
        return self._get_parameter("isLmeFutureUnderlying")

    @is_lme_future_underlying.setter
    def is_lme_future_underlying(self, value):
        self._set_parameter("isLmeFutureUnderlying", value)
