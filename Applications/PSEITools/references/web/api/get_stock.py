from Applications.PSEITools.references.web.base_api_service import *
from Applications.PSEITools.references.dto import *


class ApiServiceStock(BaseApiServicePSEITools):

    def __init__(self, source_id):
        super(ApiServiceStock, self).__init__(source_id=source_id)
        self.initialize()

    def initialize(self):
        super(ApiServiceStock, self).initialize()

    @deserialized(DtoPseStock, child='stock', wait=1)
    def get_stock_price(self, short_name: str):

        self.request.add_uri_parameter('stock', '{0}.json'.format(short_name))

        return self.send_get_request(self.request.build())


