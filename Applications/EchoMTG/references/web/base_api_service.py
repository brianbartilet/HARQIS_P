from Core.web.base import *
from Applications.load_config import *


class BaseApiServiceEchoMTG(ApiService, Generic[T]):

    def __init__(self, source_id):
        super(BaseApiServiceEchoMTG, self)\
            .__init__(app_service_type=ServiceClientType.CURL,
                      source_id=source_id,
                      apps_config_data=apps_config)

        self.username = self.parameters['username']
        self.password = self.parameters['password']

    def initialize(self):
        pass
