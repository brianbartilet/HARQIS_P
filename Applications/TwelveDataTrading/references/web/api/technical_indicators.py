from Applications.TwelveDataTrading.references.web.base_api_service import *


class ApiTechnicalIndicators(BaseApiServiceTwelveData):

    def __init__(self, source_id):
        super(ApiTechnicalIndicators, self).__init__(source_id)
        self.initialize()

    def initialize(self):
        super(ApiTechnicalIndicators, self).initialize()
        self.request.\
            add_uri_parameter('technical_indicators')

    @deserialized(dict, child='data')
    def get_all_indicators(self):
        response = self.send_get_request(self.request.build())

        return response

