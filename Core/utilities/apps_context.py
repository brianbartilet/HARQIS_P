from Core.web.api.contracts.constants.service_client_type import ServiceClientType


class AppConfigurationContext(dict):

    def __init__(self, source_id: str,
                 app_service_type: ServiceClientType,
                 source_data: dict):
        super().__init__()

        self._source_data_app_id = source_id
        self._app_service_type = app_service_type
        self._source_data = source_data

    def load_app_service_config(self) -> dict:
        return self._source_data[self._source_data_app_id][self._app_service_type.value]

    def load_app_parameters(self) -> dict:
        return self._source_data[self._source_data_app_id]['parameters']
