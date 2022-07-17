from Applications.PushNotifications import *
from Applications.load_config import *

notification_parameters = apps_config['PushNotifications']['parameters']
notification_client = BaseApiClient(**apps_config['PushNotifications']['curl'])


class TestNotifications(TestCase):

    def test_notification(self):
        curl = CurlServicePushNotifications(source_id='PushNotifications')
        curl.send_notification("Hello World")

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    @notify_work()
    def test_error(self):
        raise Exception

    @notify_work(notify_success=True)
    def test_passed(self):
        return

    def test_get_notifications(self):
        curl = CurlServicePushNotifications(source_id='PushNotifications')
        data = curl.get_notifications()
        assert_that(len(data['messages']), greater_than_or_equal_to(1))