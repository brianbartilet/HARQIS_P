from Applications.OANDA.references.web.base_api_service import *
from Applications.OANDA.references.dto import *


class ApiServiceOrders(BaseApiServiceOANDA):

    def __init__(self, source_id):
        super(ApiServiceOrders, self).__init__(source_id=source_id)
        self.initialize()

    def initialize(self):
        super(ApiServiceOrders, self).initialize()
        self.request.\
            add_uri_parameter('v3/accounts')

    @deserialized(dict)
    def get_orders(self, account_id: str, **kwargs):
        self.request\
            .add_uri_parameter(account_id)\
            .add_uri_parameter('orders')

        self.request\
            .add_query_strings(**kwargs)

        return self.send_get_request(self.request.build())

    @deserialized(dict)
    def create_order(self, account_id: str, dto):
        self.request\
            .add_uri_parameter(account_id)\
            .add_uri_parameter('orders')

        self.request\
            .add_json_body(dto)

        return self.send_post_request(self.request.build())
