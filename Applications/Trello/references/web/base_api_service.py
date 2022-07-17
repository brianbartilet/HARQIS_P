from Core.web.base import *
from Applications.load_config import *


class BaseApiServiceTrello(ApiService, Generic[T]):

    def __init__(self, source_id, **kwargs):
        super(BaseApiServiceTrello, self)\
            .__init__(app_service_type=ServiceClientType.WEBSERVICE,
                      source_id=source_id,
                      apps_config_data=apps_config,
                      **kwargs)
        self.key = self.parameters['key']
        self.token = self.parameters['token']

    def initialize(self):
        self.request \
            .add_query_string('key', self.key) \
            .add_query_string('token', self.token)