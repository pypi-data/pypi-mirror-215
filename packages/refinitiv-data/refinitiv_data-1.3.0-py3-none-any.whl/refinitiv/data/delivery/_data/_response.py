from dataclasses import dataclass
from typing import TYPE_CHECKING, List, TypeVar, Generic, Any, Union

from ._endpoint_data import Error
from ..._tools import cached_property

if TYPE_CHECKING:
    from ._data_factory import BaseDataFactory
    import httpx

TypeData = TypeVar("TypeData")


@dataclass
class BaseResponse(Generic[TypeData]):
    is_success: bool
    request_message: Union[List["httpx.Request"], "httpx.Request"]
    http_response: Union[List["httpx.Response"], "httpx.Response"]
    http_headers: Union[List["httpx.Headers"], "httpx.Headers"]
    http_status: Union[List[dict], dict]
    errors: List[Error]
    closure: Union[str, None]
    requests_count: int
    _data_factory: "BaseDataFactory"
    _kwargs: dict
    _raw: Any

    @cached_property
    def data(self) -> TypeData:
        return self._data_factory.create_data(self._raw, owner_=self, **self._kwargs)


class Response(BaseResponse[TypeData]):
    pass


def create_response(responses: List[BaseResponse], data_factory: "BaseDataFactory", kwargs: dict) -> Response:
    from ._response_factory import get_closure

    raws = []
    request_messages = []
    http_responses = []
    http_statuses = []
    http_headers = []
    errors = []
    is_success = False
    closure = None
    once = False

    for response in responses:
        is_success = is_success or response.is_success
        raws.append(response.data.raw)
        if response.errors:
            errors += response.errors
        request_messages.append(response.request_message)
        http_responses.append(response.http_response)
        http_statuses.append(response.http_status)
        http_headers.append(response.http_headers)
        if not once:
            closure = get_closure(response.http_response)
            once = True

    return Response(
        is_success,
        request_messages,
        http_responses,
        http_headers,
        http_statuses,
        errors,
        closure=closure,
        requests_count=len(responses),
        _data_factory=data_factory,
        _kwargs=kwargs,
        _raw=raws,
    )
