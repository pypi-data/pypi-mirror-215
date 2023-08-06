from ._data import NewsStoryRDPData, NewsStoryUDFData
from ._request_factory import StoryRDPRequestFactory, NewsStoryUDFRequestFactory
from ._response import NewsStoryResponse
from ._response_factory import NewsStoryResponseFactory
from .._content_validator_udf import validator
from ....delivery._data._data_provider import DataProvider

news_story_data_provider_rdp = DataProvider(
    response=NewsStoryResponseFactory(
        response_class=NewsStoryResponse,
        data_class=NewsStoryRDPData,
    ),
    request=StoryRDPRequestFactory(),
)
news_story_data_provider_udf = DataProvider(
    response=NewsStoryResponseFactory(
        response_class=NewsStoryResponse,
        data_class=NewsStoryUDFData,
    ),
    request=NewsStoryUDFRequestFactory(),
    validator=validator,
)
