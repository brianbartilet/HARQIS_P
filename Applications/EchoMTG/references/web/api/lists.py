from Applications.EchoMTG.references.web.base_api_service import *
from Applications.EchoMTG.references.dto import *
from Applications.EchoMTG.references.web.api.auth import ApiServiceEchoMTGAuth


class ApiServiceEchoMTGLists(BaseApiServiceEchoMTG):

    def __init__(self, source_id):
        super(ApiServiceEchoMTGLists, self).__init__(source_id=source_id)
        self.auth_service = ApiServiceEchoMTGAuth(source_id=source_id)
        self.access_token = self.auth_service.get_token()['token']
        self.initialize()

    def initialize(self):
        super(ApiServiceEchoMTGLists, self).initialize()
        self.request\
            .add_uri_parameter('lists')

    @deserialized(dict)
    def get_list_data(self, list_id: int):
        self.request\
            .add_uri_parameter('get')\
            .add_query_string('list', '{0}'.format(list_id))\
            .add_query_string('view', '{0}'.format('true'))\
            .add_query_string('auth', '{0}'.format(self.access_token))

        return self.send_get_request(self.request.build())
