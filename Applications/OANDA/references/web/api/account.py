from Applications.OANDA.references.web.base_api_service import *
from Applications.OANDA.references.dto import *


class ApiServiceAccount(BaseApiServiceOANDA):

    def __init__(self, source_id):
        super(ApiServiceAccount, self).__init__(source_id)
        self.initialize()

    def initialize(self):
        super(ApiServiceAccount, self).initialize()
        self.request\
            .add_uri_parameter('v3/accounts')

    @deserialized(DtoAccountProperties)
    def get_account_info(self):
        response = self.send_get_request(self.request.build())

        return response

    @deserialized(DtoAccountDetails, child='account')
    def get_account_details(self, account_id):
        self.request\
            .add_uri_parameter(account_id)

        return self.send_get_request(self.request.build())

    @deserialized(DtoAccountInstruments, child='instruments')
    def get_account_instrument_details(self, account_id, currency_name=None):
        self.request\
            .add_uri_parameter(account_id)\
            .add_uri_parameter('instruments')

        if currency_name is not None:
            self.request \
                .add_query_string('instruments', currency_name)

        return self.send_get_request(self.request.build())