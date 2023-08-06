import json
import os

from copy import copy
from typing import Dict, Any

from google.auth.transport.requests import AuthorizedSession

Session = AuthorizedSession
RequestBody = Dict[str, Any]
Response = Dict[str, Any]


class Cloud2Earth:
    """ Base class for cloud2earth """
    REQUEST = {'type': 'IMAGE', 'gcs_location': {'uris': None}}
    ENDPOINT = 'https://earthengine.googleapis.com/v1alpha/projects/{}/assets?assetId={}'

    def __init__(self, dst: str, session: Session, uri: str):
        """ Initialize Cloud2Earth class """
        self.session = session
        self.dst = dst
        self.uri = uri

    @property
    def request_body(self) -> RequestBody:
        """ Returns the request body """
        request = copy(self.REQUEST)
        request['gcs_location']['uris'] = [self.uri]
        return request
    
    @property
    def asset_name(self) -> str:
        """ Returns the asset name """
        return os.path.split(self.uri)[-1].split(".")[0]
    
    @property
    def project_folder(self):
        """ Returns the project folder """
        dest = copy(self.dst)
        return dest.split("/")[1]
    
    @property
    def assetid(self) -> str:
        """ Returns the asset id """
        return f'{self.asset_path}/{self.asset_name}'
    
    @property
    def asset_path(self) -> str:
        dst = copy(self.dst)
        return "/".join(dst.split("/")[3:])
    
    @property
    def endpoint(self):
        """ Returns a formatted endpoint """
        endpnt = copy(self.ENDPOINT)
        return endpnt.format(self.project_folder, self.assetid)
    
    def post(self) -> Response:
        response = self.session.post(
            url=self.endpoint,
            data=json.dumps(self.request_body)
        )
        return json.loads(response.content)

