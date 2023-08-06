from ...._core.session import DesktopSession
from ...._tools import extend_params
from ....delivery._data import RequestMethod
from ....delivery._data._request_factory import RequestFactory


class NewsStoryUDFRequestFactory(RequestFactory):
    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        if extended_params:
            body_parameters["Entity"]["W"].update(extended_params)
        return body_parameters

    def get_body_parameters(self, session, *args, **kwargs):
        entity = {
            "E": "News_Story",
        }
        w = dict()

        story_id = kwargs.get("story_id")
        w["storyId"] = story_id

        app_key = session.app_key
        w["productName"] = app_key

        entity["W"] = w
        body_parameters = {"Entity": entity}
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


class StoryRDPRequestFactory(RequestFactory):
    def extend_query_parameters(self, query_parameters, extended_params=None):
        return extend_params(query_parameters, extended_params)

    def get_path_parameters(self, session=None, *, story_id=None, **kwargs):
        return {"storyId": story_id}

    def get_header_parameters(self, session=None, **kwargs):
        return {"accept": "application/json"}

    def get_url(self, *args, **kwargs):
        return super().get_url(*args, **kwargs) + "/{storyId}"
