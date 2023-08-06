from .._object_definition import ObjectDefinition


class FxVolatilitySurfaceDefinition(ObjectDefinition):
    """
    The definition of the volatility surface.

    Parameters
    ----------
    fx_cross_code : str
        The currency pair of FX Cross, expressed in ISO 4217 alphabetical format
        (e.g., 'EURCHF').
    """

    def __init__(self, fx_cross_code=None):
        super().__init__()
        self.fx_cross_code = fx_cross_code

    @property
    def fx_cross_code(self):
        """
        The ISO code of the cross currency (e.g. 'EURCHF').
        Mandatory.
        :return: str
        """
        return self._get_parameter("fxCrossCode")

    @fx_cross_code.setter
    def fx_cross_code(self, value):
        self._set_parameter("fxCrossCode", value)
