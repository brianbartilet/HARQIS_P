from Core.web.base import *
from Applications.load_config import *


class BaseApiServiceCurrencyFreaks(ApiService, Generic[T]):

    def __init__(self, source_id):
        super(BaseApiServiceCurrencyFreaks, self)\
            .__init__(app_service_type=ServiceClientType.CURL,
                      source_id=source_id,
                      apps_config_data=apps_config,
                      timeout=60)

        self.api_key = self.parameters['api_key']
