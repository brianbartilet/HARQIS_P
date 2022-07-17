from Applications.OANDA.references.web.base_api_service import *
from Applications.OANDA.references.dto import *


class ApiServiceAutoChartist(BaseApiServiceOANDA):

    def __init__(self, source_id):
        super(ApiServiceAutoChartist, self).__init__(source_id=source_id)
        self.initialize()

    def initialize(self):
        super(ApiServiceAutoChartist, self).initialize()
        self.request.\
            add_uri_parameter('labs/v1/signal/autochartist')

    @deserialized(DtoAutoChartist, child='signals')
    def get_signals(self, **query_args):

        self.request.add_query_strings(**query_args)

        return self.send_get_request(self.request.build())
