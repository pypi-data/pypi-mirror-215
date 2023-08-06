import json 
import datetime
from qashared.models.extensions.divido_simple_namespace import DividoSimpleNamespace

class Route(object):
    def __init__(self):
        self.last_response = None
        self.last_response_timestamp = None
        self.required_attributes = []

    def send_request(self, request, *args, **kwargs) -> DividoSimpleNamespace:
        self.last_response, self.last_response_timestamp = request(*args, **kwargs), datetime.datetime.now().time()
        assert self.last_response.ok, f'{request.__name__.upper()} request to "{self.last_response.url}" had response status "{self.last_response.status}: {self.last_response.status_text}"'
        return json.loads(json.dumps(self.last_response.json()), object_hook=lambda d: DividoSimpleNamespace(**d)).verify_attributes(self.required_attributes, error_preface=f'{request.__name__.upper()} request to "{self.last_response.url}" had response missing the following required attributes')
