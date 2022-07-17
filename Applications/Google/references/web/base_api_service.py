from Applications.load_config import *

from .client import *


class BaseApiServiceGoogle(ApiService, Generic[T]):

    def __init__(self, source_id, client=GoogleApiClient, scopes_list=None):
        super(BaseApiServiceGoogle, self)\
            .__init__(client=client,
                      scopes_list=scopes_list,
                      app_service_type=ServiceClientType.WEBSERVICE,
                      source_id=source_id,
                      apps_config_data=apps_config)

    def initialize(self):
        ...
