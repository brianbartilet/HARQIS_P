from Applications.PushNotifications.references.web.base_api_service import *
from settings import *


def notify_work(message: str = "", source_id='PushNotifications', notify_success=False, override=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            klass_notify = CurlServicePushNotifications(source_id=source_id)
            if ENV_TESTENV == SettingsEnvironment.DEV.value and override is False:
                return func(*args, **kwargs)
            else:
                try:
                    f = func(*args, **kwargs)
                    if notify_success:
                        klass_notify.send_notification("DONE: '{0}': {1}".format(func.__name__, message))
                    return f
                except Exception as e:
                    name = type(e).__name__
                    klass_notify.send_notification("FAILED: '{0}': {1} - {2}".format(name, func.__name__ , message))
                    raise e

        return wrapper

    return decorator


class CurlServicePushNotifications(BaseApiServicePushNotifications):

    def __init__(self, source_id):
        super().__init__(source_id=source_id)
        self.initialize()

    def send_notification(self, message):
        self.request\
            .add_payload(message, PayloadType.TEXT)

        return self.send_post_request(self.request.build())

    @deserialized(dict)
    def get_notifications(self):
        self.request.add_uri_parameter('json')

        return self.send_get_request(self.request.build())

