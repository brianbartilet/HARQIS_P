from Core.web.base import *
from Applications.load_config import *


class BaseApiServiceExchangeRates(ApiService, Generic[T]):

    def __init__(self, source_id):
        super(BaseApiServiceExchangeRates, self)\
            .__init__(app_service_type=ServiceClientType.WEBSERVICE,
                      source_id=source_id,
                      apps_config_data=apps_config)

        self.access_key = self.parameters.get('access_key', None)

    def initialize(self):
        self.request\
            .add_header('Authorization', 'Basic {0}'.format(self.access_key))

