from typing import List

from ._data import NewsHeadlinesUDFData, NewsHeadlinesRDPData
from ._request_factory import (
    NewsHeadlinesRDPRequestFactory,
    NewsHeadlinesUDFRequestFactory,
)
from .._content_validator_udf import validator
from .._df_builder import concat_news_dfs
from ..._content_data_factory import ContentDataFactory
from ..._content_data_provider import ContentDataProvider
from ..._content_response_factory import ContentResponseFactory
from ....delivery._data._response import create_response, BaseResponse

MAX_LIMIT = 100


class NewsDataFactoryMultiResponse(ContentDataFactory):
    def get_dfbuilder(self, **__):
        return concat_news_dfs


class NewsHeadlinesDataProvider(ContentDataProvider):
    data_factory_multi_response: NewsDataFactoryMultiResponse

    @classmethod
    def create_response(cls, responses: List[BaseResponse], limit: int, kwargs: dict) -> BaseResponse:
        if len(responses) == 1:
            response = responses[0]
            response.data._limit = limit
            return response

        kwargs["responses"] = responses
        kwargs["limit"] = limit
        response = create_response(responses, cls.data_factory_multi_response, kwargs)
        response.data._limit = limit
        return response


class NewsHeadlinesUDFDataProvider(NewsHeadlinesDataProvider):
    data_factory_multi_response = NewsDataFactoryMultiResponse(NewsHeadlinesUDFData)

    @staticmethod
    def change_count(count: int, limit: int, kwargs: dict):
        number = abs(limit - count)
        if number < MAX_LIMIT:
            kwargs["count"] = number

    def get_data(self, *args, **kwargs):
        limit = kwargs.get("count")

        if limit is None:
            response = super().get_data(*args, **kwargs)

        else:
            responses = []
            headlines = True
            count = 0

            if limit > MAX_LIMIT:
                kwargs["count"] = MAX_LIMIT

            while count < limit and headlines:
                response = super().get_data(*args, **kwargs)
                headlines = response.data.raw.get("headlines", [])
                count += len(headlines)
                kwargs["payload"] = response.data.raw.get("older")
                responses.append(response)
                self.change_count(count, limit, kwargs)

            response = self.create_response(responses, limit, kwargs)

        return response

    async def get_data_async(self, *args, **kwargs):
        limit = kwargs.get("count")

        if limit is None:
            response = await super().get_data_async(*args, **kwargs)

        else:
            responses = []
            headlines = True
            count = 0

            if limit > MAX_LIMIT:
                kwargs["count"] = MAX_LIMIT

            while count < limit and headlines:
                response = await super().get_data_async(*args, **kwargs)
                headlines = response.data.raw.get("headlines", [])
                count += len(headlines)
                kwargs["payload"] = response.data.raw.get("older")
                responses.append(response)
                self.change_count(count, limit, kwargs)

            response = self.create_response(responses, limit, kwargs)

        return response


class NewsHeadlinesRDPDataProvider(NewsHeadlinesDataProvider):
    data_factory_multi_response = NewsDataFactoryMultiResponse(NewsHeadlinesRDPData)

    def get_data(self, *args, **kwargs):
        on_page_response = kwargs.get("on_page_response")
        limit = kwargs.get("count")
        responses = []
        cursor = True
        count = 0

        if limit > MAX_LIMIT:
            kwargs["count"] = MAX_LIMIT

        while count < limit and cursor:
            response = super().get_data(*args, **kwargs)
            responses.append(response)

            if on_page_response:
                on_page_response(self, response)

            meta = response.data.raw.get("meta", {})
            count += meta.get("count", 0)
            cursor = meta.get("next")
            kwargs = {
                "cursor": cursor,
                "__content_type__": kwargs.get("__content_type__"),
            }

        return self.create_response(responses, limit, kwargs)

    async def get_data_async(self, *args, **kwargs):
        on_page_response = kwargs.get("on_page_response")
        limit = kwargs.get("count")
        responses = []
        cursor = True
        count = 0

        if limit > MAX_LIMIT:
            kwargs["count"] = MAX_LIMIT

        while count < limit and cursor:
            response = await super().get_data_async(*args, **kwargs)
            responses.append(response)

            if on_page_response:
                on_page_response(self, response)

            meta = response.data.raw.get("meta", {})
            count += meta.get("count", 0)
            cursor = meta.get("next")
            kwargs = {
                "cursor": cursor,
                "__content_type__": kwargs.get("__content_type__"),
            }

        return self.create_response(responses, limit, kwargs)


news_headlines_data_provider_rdp = NewsHeadlinesRDPDataProvider(
    response=ContentResponseFactory(data_class=NewsHeadlinesRDPData),
    request=NewsHeadlinesRDPRequestFactory(),
)
news_headlines_data_provider_udf = NewsHeadlinesUDFDataProvider(
    response=ContentResponseFactory(data_class=NewsHeadlinesUDFData),
    request=NewsHeadlinesUDFRequestFactory(),
    validator=validator,
)
