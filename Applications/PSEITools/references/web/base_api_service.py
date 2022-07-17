from Core.web.base import *
from Applications.load_config import *


class BaseApiServicePSEITools(ApiService, Generic[T]):

    def __init__(self, source_id):
        super(BaseApiServicePSEITools, self)\
            .__init__(app_service_type=ServiceClientType.WEBSERVICE,
                      source_id=source_id,
                      apps_config_data=apps_config)

    def initialize(self):
        self.request \
            .add_header('Content-Type', 'application/json')