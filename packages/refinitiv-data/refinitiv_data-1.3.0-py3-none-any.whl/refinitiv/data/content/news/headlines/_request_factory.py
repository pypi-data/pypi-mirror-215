from . import SortOrder

from ...._core.session import DesktopSession
from ...._tools import (
    make_enum_arg_parser,
    ParamItem,
    ValueParamItem,
    to_iso_format,
    extend_params,
)
from ....delivery._data import RequestMethod
from ....delivery._data._request_factory import RequestFactory

sort_order_news_arg_parser = make_enum_arg_parser(SortOrder)
news_headlines_query_parameters = [
    ParamItem("query"),
    ParamItem("count", "limit"),
    ValueParamItem("date_from", "dateFrom", to_iso_format),
    ValueParamItem("date_to", "dateTo", to_iso_format),
    ValueParamItem("sort_order", "sort", sort_order_news_arg_parser.get_str),
    ParamItem("cursor"),
]


class NewsHeadlinesRDPRequestFactory(RequestFactory):
    def extend_query_parameters(self, query_parameters, extended_params=None):
        return extend_params(query_parameters, extended_params)

    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        return body_parameters

    @property
    def query_params_config(self):
        return news_headlines_query_parameters


news_headlines_body_parameters = [
    ParamItem("query"),
    ValueParamItem("count", "number", str),
    ValueParamItem(
        "payload",
        function=lambda payload: payload.replace("/headlines?payload=", "", 1),
    ),
    ParamItem("repository"),
    ParamItem(
        "query",
        "productName",
        function=lambda _, session, *args, **kwargs: session.app_key,
    ),
    ValueParamItem("date_from", "dateFrom", to_iso_format),
    ValueParamItem("date_to", "dateTo", to_iso_format),
]


class NewsHeadlinesUDFRequestFactory(RequestFactory):
    @property
    def body_params_config(self):
        return news_headlines_body_parameters

    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        if extended_params:
            body_parameters["Entity"]["W"].update(extended_params)
        return body_parameters

    def get_body_parameters(self, *args, **kwargs):
        w = super().get_body_parameters(*args, **kwargs)

        body_parameters = {"Entity": {"E": "News_Headlines", "W": dict(w)}}
        return body_parameters

    def get_url(self, session, *args, **kwargs):
        url = session._get_rdp_url_root()
        if isinstance(session, DesktopSession):
            url = session._get_udf_url()
        return url

    def update_url(self, url_root, url, path_parameters, query_parameters):
        return url

    def get_request_method(self, **kwargs) -> RequestMethod:
        return RequestMethod.POST
