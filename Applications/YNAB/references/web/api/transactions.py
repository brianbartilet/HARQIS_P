from Applications.YNAB.references.web.base_api_service import *
from Applications.YNAB.references.dto import *


class ApiServiceYNABTransactions(BaseApiServiceYouNeedABudget):

    def initialize(self):
        super(ApiServiceYNABTransactions, self).initialize()
        self.request\
            .add_uri_parameter('budgets')

    @deserialized(dict, child='data')
    def get_transactions(self, budget_id):
        self.request\
            .add_uri_parameter(budget_id)\
            .add_uri_parameter('transactions')

        return self.send_get_request(self.request.build())

    @deserialized(dict, child='data')
    def get_transactions_per_account(self, budget_id, account_id):
        self.request\
            .add_uri_parameter(budget_id)\
            .add_uri_parameter('accounts')\
            .add_uri_parameter('{0}'.format(account_id))\
            .add_uri_parameter('transactions')

        return self.send_get_request(self.request.build())

    @deserialized(dict, child='data')
    def create_new_transaction(self, budget_id, transaction):

        self.request\
            .add_uri_parameter(budget_id)\
            .add_uri_parameter('transactions')\
            .add_json_body(transaction)

        return self.send_post_request(self.request.build())

    @deserialized(dict, child='data')
    def update_transaction(self, budget_id, transaction):

        self.request\
            .add_uri_parameter(budget_id)\
            .add_uri_parameter('transactions')\
            .add_json_body(transaction)

        return self.send_patch_request(self.request.build())

