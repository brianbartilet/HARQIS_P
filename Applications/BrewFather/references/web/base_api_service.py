from Core.web.base import *
from Applications.load_config import *


class BaseApiServiceBrewFather(ApiService, Generic[T]):

    def __init__(self, source_id):
        super(BaseApiServiceBrewFather, self)\
            .__init__(app_service_type=ServiceClientType.CURL,
                      source_id=source_id,
                      apps_config_data=apps_config,
                      timeout=60)

        self.access_key = self.parameters['access_key']

    def initialize(self):
        self.request\
            .add_header('Authorization', 'Basic {0}'.format(self.access_key))
