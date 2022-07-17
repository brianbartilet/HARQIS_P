from Applications.BrewFather.references.web.base_api_service import *
from Applications.BrewFather.references.dto import *


class ApiServiceBrewFatherBatches(BaseApiServiceBrewFather):

    def __init__(self, source_id):
        super(ApiServiceBrewFatherBatches, self).__init__(source_id=source_id)
        self.initialize()

    def initialize(self):
        super(ApiServiceBrewFatherBatches, self).initialize()
        self.request\
            .add_uri_parameter('batches')

    @deserialized(dict)
    def get_batches(self, include="", complete=False, status='Planning', offset=0, limit=10):
        self.request\
            .add_query_string('complete', complete) \
            .add_query_string('include', include) \
            .add_query_string('status', status)\
            .add_query_string('offset', offset)\
            .add_query_string('limit', limit)

        return self.send_get_request(self.request.build())

    @deserialized(dict)
    def get_batch_information(self, id, include=""):
        self.request\
            .add_uri_parameter(id)\
            .add_query_string('include', include)

        return self.send_get_request(self.request.build())

    @deserialized(dict)
    def get_batch_readings(self, id):
        self.request\
            .add_uri_parameter(id)\
            .add_uri_parameter('readings')

        return self.send_get_request(self.request.build())

    @deserialized(dict)
    def get_batch_last_reading(self, id):
        self.request\
            .add_uri_parameter(id) \
            .add_uri_parameter('readings') \
            .add_uri_parameter('last')

        return self.send_get_request(self.request.build())

    @deserialized(dict)
    def get_batch_brewtracker(self, id):
        self.request\
            .add_uri_parameter(id)\
            .add_uri_parameter('brewtracker')

        return self.send_get_request(self.request.build())

