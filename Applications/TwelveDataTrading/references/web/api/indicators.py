from Applications.TwelveDataTrading.references.web.base_api_service import *
from Applications.TwelveDataTrading.references.dto import *


class ApiIndicatorsFeed(BaseApiServiceTwelveData):
    """



    """
    def __init__(self, source_id, indicator_short_name):
        super(ApiIndicatorsFeed, self).__init__(source_id)
        self.indicator_short_name = indicator_short_name
        self.initialize()

    def initialize(self):
        super(ApiIndicatorsFeed, self).initialize()
        self.request.\
            add_uri_parameter(str(self.indicator_short_name).lower())

    @deserialized(dict)
    def get_indicator_values(self, dto: IndicatorParameters):
        self.request.add_query_object(dto)
        response = self.send_get_request(self.request.build())

        return response
