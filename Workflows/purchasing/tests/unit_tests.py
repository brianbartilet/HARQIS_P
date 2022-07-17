from Workflows.purchasing import *


class UnitTests(TestCase):

    def test_create_order(self):
        execute_orders(
            nike_id='NikeOrder1',
            trello_id='Trello',
            notifications_id='PushNotifications',
            board_name='Nike Order Robot',
            pending_list_name='PENDING',
        )

