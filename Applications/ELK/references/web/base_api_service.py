from Core.web.base import *
from Applications import *


class BaseApiServiceElasticSearch(ApiService, Generic[T]):

    def __init__(self, source_id, **kwargs):
        super(BaseApiServiceElasticSearch, self)\
            .__init__(app_service_type=ServiceClientType.WEBSERVICE,
                      source_id=source_id,
                      apps_config_data=apps_config,
                      **kwargs)