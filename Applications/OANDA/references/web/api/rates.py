from Applications.OANDA.references.web.base_api_service import *
from Applications.OANDA.references.dto import *


class ApiServiceRates(BaseApiServiceOANDA):

    def __init__(self, source_id):
        super(ApiServiceRates, self).__init__(source_id=source_id)
        self.initialize()

    def initialize(self):
        super(ApiServiceRates, self).initialize()
        self.request.\
            add_uri_parameter(type(self).__name__, 'v1/instruments')

    @deserialized(dict)
    def get_rate(self, account_id: str, instrument: str):

        self.request\
            .add_query_string('accountId', account_id)\
            .add_query_string('instruments', instrument)

        return self.send_get_request(self.request.build())
