from typing import TYPE_CHECKING

from ._chain import default_error_message
from ._universe_expander import UniverseExpander
from ..._core.session import get_default
from ..._errors import RDError
from ..._tools import DEBUG
from ..._tools import cached_property
from ...content import fundamental_and_reference
from ...content._content_data import Data

if TYPE_CHECKING:
    from logging import Logger


def update_universe(raw, _universe):
    index = 0  # instrument
    data = raw.get("data")
    if data and all(isinstance(i[index], str) for i in data):
        universe = [i[index] for i in data]
    else:
        universe = _universe
    return universe


def get_universe(expression):
    session = get_default()
    logger = session.logger()
    adc_data = get_adc_data(
        params={
            "universe": expression,
            "fields": "TR.RIC",
        },
        logger=logger,
    )
    adc_raw = adc_data.raw
    return update_universe(
        adc_raw,
        None,
    )


def get_adc_data(params: dict, logger: "Logger") -> Data:
    """
    Gets data from ADC endpoint.

    Parameters
    ----------
    params : dict
        API request parameters.
    logger : Logger
        Session logger.

    Returns
    -------
    response : Data
        API response data.

    """
    fields = params.get("fields", "")
    universe = params["universe"]
    logger.info(f"Requesting {fields} for {universe}")
    response = fundamental_and_reference.Definition(**params).get_data()
    DEBUG and logger.debug(f"ADC --->\n{response.data.df.to_string()}\n")

    request_messages = response.request_message
    statuses = response.http_status

    if not isinstance(response.request_message, list):
        request_messages = [response.request_message]
        statuses = [response.http_status]

    for request, status in zip(request_messages, statuses):
        path = request.url.path
        current_universe = path.rsplit("/", 1)[-1]
        if current_universe not in universe:
            current_universe = universe
        logger.info(f"Request to {path} with {fields} for {current_universe}\nstatus: {status}\n")

    return response.data


class DiscoveryUniverse(UniverseExpander):
    def __init__(self, expression):
        self._expression = expression

    @property
    def expression(self):
        return self._expression

    @cached_property
    def _universe(self):
        universe = get_universe(self._expression)
        if not universe:
            raise RDError(-1, default_error_message)
        return universe
