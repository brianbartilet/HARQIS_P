from Applications.EchoMTG.references.web.base_api_service import *
from Applications.EchoMTG.references.dto import *


class ApiServiceEchoMTGAuth(BaseApiServiceEchoMTG):

    def __init__(self, source_id):
        super(ApiServiceEchoMTGAuth, self).__init__(source_id=source_id)
        self.initialize()
        self.auth_headers = {}

    def initialize(self):
        super(ApiServiceEchoMTGAuth, self).initialize()
        self.request\
            .add_uri_parameter('user')\
            .add_uri_parameter('auth')

    @deserialized(dict)
    def get_token(self):
        response = self.authenticate()
        self.auth_headers = response.headers

        return response

    def authenticate(self):
        self.request \
            .add_query_string('email', self.username) \
            .add_query_string('type', 'curl') \
            .add_query_string('password', self.password)

        response = self.send_post_request(self.request.build())
        response.headers.update({'Content-Type': 'application/json'})

        return response
