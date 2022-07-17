from Core.web.base import *
from Applications.load_config import *


class BaseApiServicePushNotifications(ApiService, Generic[T]):

    def __init__(self, source_id):
        super(BaseApiServicePushNotifications, self)\
            .__init__(app_service_type=ServiceClientType.CURL,
                      source_id=source_id,
                      apps_config_data=apps_config,
                      timeout=60)

        self.notification_id = self.parameters['notification_id']

    def initialize(self):
        self.request \
            .add_uri_parameter(self.notification_id)
