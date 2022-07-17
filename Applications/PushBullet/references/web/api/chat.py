from Applications.PushBullet.references.web.base_api_service import *
from Applications.PushBullet.references.dto import *


class ApiServicePushBulletChat(BaseApiServicePushBullet):

    def __init__(self, source_id):
        super(ApiServicePushBulletChat, self).__init__(source_id)
        self.initialize()

    def initialize(self):
        super(ApiServicePushBulletChat, self).initialize()
        self.request\
            .add_uri_parameter('v2/permanents')

    @deserialized(dict)
    def get_threads(self):

        self.request\
            .add_uri_parameter('{0}_threads'.format(self.device_id))

        return self.send_get_request(self.request.build())

    @deserialized(dict)
    def get_thread_items(self, thread_id: int):

        self.request\
            .add_uri_parameter('{0}_thread_{1}'.format(self.device_id, thread_id))

        return self.send_get_request(self.request.build())
