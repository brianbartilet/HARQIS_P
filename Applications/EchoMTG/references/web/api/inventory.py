from Applications.EchoMTG.references.web.base_api_service import *
from Applications.EchoMTG.references.dto import *
from Applications.EchoMTG.references.web.api.auth import ApiServiceEchoMTGAuth


class ApiServiceEchoMTGInventory(BaseApiServiceEchoMTG):

    def __init__(self, source_id):
        super(ApiServiceEchoMTGInventory, self).__init__(source_id=source_id)
        self.auth_service = ApiServiceEchoMTGAuth(source_id=source_id)
        self.access_token = self.auth_service.get_token()['token']
        self.initialize()

    def initialize(self):
        super(ApiServiceEchoMTGInventory, self).initialize()
        self.request\
            .add_uri_parameter('inventory')

    @deserialized(dict)
    def get_collection(self, start=0, limit=10000):
        self.request\
            .add_uri_parameter('view')\
            .add_query_string('start', start)\
            .add_query_string('limit', limit)\
            .add_query_string('auth', '{0}'.format(self.access_token))

        return self.send_get_request(self.request.build())

    @deserialized(dict)
    def get_collection_dump(self, show_deleted=True):
        self.request\
            .add_uri_parameter('dump') \
            .add_query_string('showDeleted', '{0}'.format(show_deleted).lower())\
            .add_query_string('auth', '{0}'.format(self.access_token))\
            .strip_right_url(False)

        return self.send_get_request(self.request.build())

    @deserialized(dict)
    def update_acquired_date(self, inventory_id, date_mm_dd_yyyy):
        self.request\
            .add_uri_parameter('adjust_date')\
            .add_query_string('id', inventory_id)\
            .add_query_string('value', date_mm_dd_yyyy)\
            .add_query_string('auth', '{0}'.format(self.access_token))

        return self.send_put_request(self.request.build())

    @deserialized(dict)
    def update_toggle_tradable(self, inventory_id: str, to_trade_toggle: bool):
        toggle_value = 1 if to_trade_toggle else 0
        self.request\
            .add_uri_parameter('toggle_tradable')\
            .add_query_string('id', inventory_id)\
            .add_query_string('toggle_tradable', toggle_value)\
            .add_query_string('auth', '{0}'.format(self.access_token))\
            .strip_right_url(False)

        return self.send_post_request(self.request.build())

    @deserialized(dict)
    def add_card_to_collection(self, card_dto: DtoEchoMTGCard):
        self.request \
            .add_header(HttpHeaders.AUTHORIZATION.value, 'Bearer {0}'.format(self.access_token))\
            .add_uri_parameter('add')\
            .add_query_object(card_dto)

        return self.send_post_request(self.request.build())