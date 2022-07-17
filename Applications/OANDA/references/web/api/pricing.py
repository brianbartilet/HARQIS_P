from Applications.OANDA.references.web.base_api_service import *
from Applications.OANDA.references.dto import *


class ApiServicePricing(BaseApiServiceOANDA):

    def __init__(self, source_id):
        super(ApiServicePricing, self).__init__(source_id=source_id)
        self.initialize()

    def initialize(self):
        super(ApiServicePricing, self).initialize()
        self.request.\
            add_uri_parameter(type(self).__name__, 'v3/accounts')

    @deserialized(DtoPrice, child='prices')
    def get_pricing(self, account_id: str, list_instruments: str):

        self.request\
            .add_uri_parameter('account_number', account_id)\
            .add_uri_parameter('pricing', 'pricing')

        self.request\
            .add_query_string('instruments', list_instruments)

        return self.send_get_request(self.request.build())
