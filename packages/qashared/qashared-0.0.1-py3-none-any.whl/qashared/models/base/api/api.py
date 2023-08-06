from playwright.sync_api import APIRequestContext
from typing import Generator
from qashared.models.base.api.route import Route

class Api(object):
    def __init__(self, base_url, headers) -> None:
        self.base_url = base_url
        self.headers = headers

    def get_context(self, playwright) -> Generator[APIRequestContext, None, None]:
        request_context = playwright.request.new_context(base_url=self.base_url, extra_http_headers=self.headers)
        yield request_context
        request_context.dispose()

    @property
    def routes(self):
        return [value for value in self.__dict__.values() if isinstance(value, Route)]
    
    @property
    def last_response(self):
        latest_route = max(self.routes, key=lambda route: route.last_response_timestamp, default=None)
        return latest_route.last_response if latest_route else None
