from Applications.BPI.references.web.base_api_service import *
from Applications.BPI.references.dto import *


class ApiServiceBPIAccountDetails(BaseApiServiceBPI):

    def __init__(self, source_id, driver):
        super(ApiServiceBPIAccountDetails, self).__init__(source_id=source_id, driver=driver)
        self.initialize()

    def initialize(self):
        super(ApiServiceBPIAccountDetails, self).initialize()
        self.request.\
            add_uri_parameter('account-details')

    #@deserialized(dict, child='trades')
    def get_account_details(self, account_type, productId):

        self.request\
            .add_query_string('accountType', account_type)\
            .add_query_string('productId', productId)

        x = self.send_get_request(self.request.build())
        return x
