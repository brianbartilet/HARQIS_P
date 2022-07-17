from Applications.YNAB.references.web.base_api_service import *
from Applications.YNAB.references.dto import *


class ApiServiceYNABCategories(BaseApiServiceYouNeedABudget):

    def initialize(self):
        super(ApiServiceYNABCategories, self).initialize()
        self.request\
            .add_uri_parameter('budgets')

    @deserialized(dict, child='data')
    def get_categories(self, budget_id):
        self.request\
            .add_uri_parameter(budget_id)\
            .add_uri_parameter('categories')

        return self.send_get_request(self.request.build())