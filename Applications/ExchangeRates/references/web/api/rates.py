from Applications.ExchangeRates.references.web.base_api_service import *
from Applications.ExchangeRates.references.dto import *


class ApiServiceTradesRates(BaseApiServiceExchangeRates):

    def __init__(self, source_id):
        super(ApiServiceTradesRates, self).__init__(source_id=source_id)
        self.initialize()

    def initialize(self):
        super(ApiServiceTradesRates, self).initialize()

    @deserialized(dict, child='batchList')
    def get_rates(self, from_currency, to_currency, **kwargs):

        self.request \
            .add_uri_parameter('charting-rates')\
            .add_query_string('fromCurrency', from_currency)\
            .add_query_string('toCurrency', to_currency)\

        self.request.add_query_strings(**kwargs)

        return self.send_get_request(self.request.build())

    def get_current_rate(self, from_currency, to_currency, round_to=2, **kwargs):

        values = self.get_rates(from_currency, to_currency, **kwargs)
        actual = values[-1]['rates'][-1] - values[-1]['rates'][0]

        return round(actual, round_to)



