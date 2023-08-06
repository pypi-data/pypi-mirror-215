from typing import Optional

from ..._object_definition import ObjectDefinition


class ParRateShift(ObjectDefinition):
    """
    Parameters
    ----------
    cross_currency_instruments : dict, optional
        The list of shift attributes applied to the zero coupon curve constructed from
        cross currency instrument constituents.
    interest_rate_instruments : dict, optional
        The list of shift attributes applied to curve constructed from interest rate
        instrument constituents.
    """

    def __init__(
        self,
        *,
        cross_currency_instruments: Optional[dict] = None,
        interest_rate_instruments: Optional[dict] = None,
    ) -> None:
        super().__init__()
        self.cross_currency_instruments = cross_currency_instruments
        self.interest_rate_instruments = interest_rate_instruments

    @property
    def cross_currency_instruments(self):
        """
        The list of shift attributes applied to the zero coupon curve constructed from
        cross currency instrument constituents.
        :return: dict
        """
        return self._get_parameter("crossCurrencyInstruments")

    @cross_currency_instruments.setter
    def cross_currency_instruments(self, value):
        self._set_parameter("crossCurrencyInstruments", value)

    @property
    def interest_rate_instruments(self):
        """
        The list of shift attributes applied to curve constructed from interest rate
        instrument constituents.
        :return: dict
        """
        return self._get_parameter("interestRateInstruments")

    @interest_rate_instruments.setter
    def interest_rate_instruments(self, value):
        self._set_parameter("interestRateInstruments", value)
