from Applications.OANDA.references.web.base_api_service import *
from Applications.OANDA.references.dto import *


class ApiServiceTrades(BaseApiServiceOANDA):

    def __init__(self, source_id):
        super(ApiServiceTrades, self).__init__(source_id=source_id)
        self.initialize()

    def initialize(self):
        super(ApiServiceTrades, self).initialize()
        self.request.\
            add_uri_parameter('v3/accounts')

    @deserialized(DtoAccountProperties, child='trades')
    def get_trades_from_account(self, account_id, **kwargs):

        self.request\
            .add_uri_parameter(account_id)\
            .add_uri_parameter('trades')\
            .add_query_strings(**kwargs)

        return self.send_get_request(self.request.build())

    @deserialized(DtoAccountProperties, child='trades')
    def get_open_trades_from_account(self, account_id):

        self.request\
            .add_uri_parameter(account_id)\
            .add_uri_parameter('openTrades')

        return self.send_get_request(self.request.build())