from Core.web.base import *
from Applications.load_config import *


class BaseApiServiceYouNeedABudget(ApiService, Generic[T]):

    def __init__(self, source_id):
        super(BaseApiServiceYouNeedABudget, self)\
            .__init__(app_service_type=ServiceClientType.WEBSERVICE,
                      apps_config_data=apps_config,
                      source_id=source_id)

        self.access_token = self.parameters.get('access_token', None)

    def initialize(self):
        self.request \
            .add_query_string('access_token', self.access_token) \
            .add_header('Content-Type', 'application/json')
