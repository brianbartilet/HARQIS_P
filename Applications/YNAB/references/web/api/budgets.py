from Applications.YNAB.references.web.base_api_service import *
from Applications.YNAB.references.dto import *


class ApiServiceYNABBudgets(BaseApiServiceYouNeedABudget):

    def initialize(self):
        super(ApiServiceYNABBudgets, self).initialize()
        self.request\
            .add_uri_parameter('budgets')

    @deserialized(dict, child='data')
    def get_budgets(self):
        return self.send_get_request(self.request.build())

    @deserialized(dict, child='data')
    def get_budget_info(self, budget_id):
        self.request\
            .add_uri_parameter(budget_id)
        return self.send_get_request(self.request.build())
