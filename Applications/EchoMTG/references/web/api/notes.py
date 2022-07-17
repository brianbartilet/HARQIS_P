from Applications.EchoMTG.references.web.base_api_service import *
from Applications.EchoMTG.references.dto import *
from Applications.EchoMTG.references.web.api.auth import ApiServiceEchoMTGAuth


class ApiServiceEchoMTGNotes(BaseApiServiceEchoMTG):

    def __init__(self, source_id):
        super(ApiServiceEchoMTGNotes, self).__init__(source_id=source_id)
        self.auth_service = ApiServiceEchoMTGAuth(source_id=source_id)
        self.access_token = self.auth_service.get_token()['token']
        self.initialize()

    def initialize(self):
        super(ApiServiceEchoMTGNotes, self).initialize()
        self.request\
            .add_uri_parameter('notes')

    @deserialized(dict)
    def get_note(self, note_id: str):
        self.request\
            .add_uri_parameter('note')\
            .add_query_string('id', note_id)\
            .add_query_string('auth', '{0}'.format(self.access_token))

        return self.send_get_request(self.request.build())

    @deserialized(dict)
    def create_note(self, inventory_id: str, note: str):

        payload = {
            'note': note,
            'inventory_id': inventory_id,
            'auth': self.access_token
        }

        self.request\
            .add_uri_parameter('create')\
            .add_payload(payload, PayloadType.TEXT)\
            .strip_right_url(False)

        return self.send_post_request(self.request.build())

    @deserialized(dict)
    def update_note(self, note_id: str, note: str):

        payload = {
            'note': note,
            'note_id': note_id,
            'auth': self.access_token
        }

        self.request \
            .add_uri_parameter('edit')\
            .add_payload(payload, PayloadType.TEXT)\
            .strip_right_url(False)

        return self.send_post_request(self.request.build())

