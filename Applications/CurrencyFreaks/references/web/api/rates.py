from Applications.CurrencyFreaks.references.web.base_api_service import *


class ApiServiceCurrencyFreaksRates(BaseApiServiceCurrencyFreaks):

    def __init__(self, source_id):
        super(ApiServiceCurrencyFreaksRates, self).__init__(source_id=source_id)
        self.initialize()

    def initialize(self):
        super(ApiServiceCurrencyFreaksRates, self).initialize()
        self.request\
            .add_uri_parameter('latest') \
            .add_query_string('apikey', self.api_key)  # atest?apikey=YOUR_APIKEY'

    @deserialized(dict)
    def get_latest_rates(self):
        return self.send_get_request(self.request.build())

