from Applications.YNAB.references.web.base_api_service import *
from Applications.YNAB.references.dto import *


class ApiServiceYNABUser(BaseApiServiceYouNeedABudget):

    def initialize(self):
        super(ApiServiceYNABUser, self).initialize()
        self.request\
            .add_uri_parameter('user')

    @deserialized(dict)
    def get_user_info(self):
        return self.send_get_request(self.request.build())


