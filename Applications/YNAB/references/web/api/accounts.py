from Applications.YNAB.references.web.base_api_service import *
from Applications.YNAB.references.dto import *


class ApiServiceYNABAccounts(BaseApiServiceYouNeedABudget):

    def initialize(self):
        super(ApiServiceYNABAccounts, self).initialize()
        self.request\
            .add_uri_parameter('budgets')

    @deserialized(dict, child='data')
    def get_accounts(self, budget_id):
        self.request\
            .add_uri_parameter(budget_id)\
            .add_uri_parameter('accounts')

        return self.send_get_request(self.request.build())

    @deserialized(dict, child='data')
    def create_new_account(self, budget_id, acc: DtoSaveAccountWrapper):

        self.request\
            .add_uri_parameter(budget_id)\
            .add_uri_parameter('accounts')\
            .add_json_body(acc)

        return self.send_post_request(self.request.build())


