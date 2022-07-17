from Core.web.base import *
from Applications.load_config import *


class BaseApiServiceTwelveData(ApiService, Generic[T]):

    def __init__(self, source_id):
        super(BaseApiServiceTwelveData, self)\
            .__init__(app_service_type=ServiceClientType.WEBSERVICE,
                      source_id=source_id,
                      apps_config_data=apps_config)
        self.api_key = self.parameters['api_key']

    def initialize(self):
        self.request \
            .add_query_string('apikey', self.api_key)
