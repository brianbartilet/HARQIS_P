from Core.web.base import *
from Applications.load_config import *


class BaseApiServicePushBullet(ApiService, Generic[T]):

    def __init__(self, source_id, **kwargs):
        super(BaseApiServicePushBullet, self)\
            .__init__(app_service_type=ServiceClientType.WEBSERVICE,
                      source_id=source_id,
                      apps_config_data=apps_config,
                      **kwargs)

        self.access_token = self.parameters['access_token']
        self.device_id = self.parameters['device_id']

    def initialize(self):
        self.request \
            .add_header('Access-Token', self.access_token)