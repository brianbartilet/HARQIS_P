from Applications.PushBullet.references import *


class TestsPushBullet(TestCase):

    def test_threads(self):
        service = ApiServicePushBulletChat(source_id='PushBullet')
        response = service.get_threads()
        assert_that(len(response['threads']), greater_than(1))

    def test_threads_chat_info(self):
        service = ApiServicePushBulletChat(source_id='PushBullet')
        response = service.get_threads()
        id = QList(response['threads']).first()['id']
        response = service.get_thread_items(id)
        assert_that(len(response['thread']), greater_than(1))


