from Applications import *

import datetime
import dateutil.parser
import pytz
import yaml

LIST_RUNNING = "RUNNING - DO NOT TOUCH"
LIST_SUCCESS = "ORDERED"
LIST_FAILED = "FAILED"
POLLING_IN_MINUTES_TRIGGER = 20


def execute_order_nike_front_end(nike_id, details):

    driver = WebDriverFactory.get_web_driver_instance(**apps_config[nike_id]['webdriver'])
    pl = PageLoginNike(driver=driver, source_id=nike_id)
    pl.login(pl.parameters['username'], pl.parameters['password'])

    pi = PageItemNike(driver=driver,
                      source_id=nike_id,
                      item_url=details['link'],
                      max_time_wait_mins=POLLING_IN_MINUTES_TRIGGER)

    pi.wait_for_item_availability()
    pi.select_order_details(details['size'])
    pi.go_to_cart()

    pc = PageCartNike(driver=driver, source_id=nike_id,
                      payment_details=apps_config[nike_id]['payment_details'])
    pc.member_checkout()
    pc.payment_checkout()



    #pl.logout()
    #pl.driver.close()

    return False


@app.task()
def execute_orders(nike_id, trello_id, notifications_id, board_name, pending_list_name):

    trello_cards_service = ApiServiceCards(trello_id)
    trello_boards_service = ApiServiceBoards(trello_id)
    notification = CurlServicePushNotifications(notifications_id)
    current_cards, id_list, target_board = get_board_data(trello_id, board_name, pending_list_name)

    """
    Pick first card
    Change id list, Move to LIST_RUNNING
    Check if order is due in the next 15 mins
    """

    task_card = None
    for card in current_cards:
        if card.due is None:
            log.warning("Card without due date {0} in {1}".format(card.name, pending_list_name))
            notification.send_notification("{0}: Card without due date {1}".format(board_name, card.name))
            continue

        #  check details for account matching
        details_account = yaml.load(card.desc)
        if details_account['size'] != apps_config[nike_id]['parameters']['size']:
            continue

        due_date = dateutil.parser.parse(card.due)
        diff_date = pytz.utc.localize(datetime.datetime.utcnow()) - due_date

        if diff_date.days == -1:
            countdown_hours = 24 - (diff_date.seconds // 3600)
            countdown_mins = (60 - ((diff_date.seconds % 3600) // 60))
            if (countdown_hours < 2) and (countdown_mins < POLLING_IN_MINUTES_TRIGGER):
                task_card = card
                break
        elif diff_date.days >= 0:
            task_card = card
            break
        else:
            continue

    details = None
    updated_card = None

    if task_card is not None:
        id_list_to = QList(trello_boards_service.get_board_lists(target_board)) \
            .first(lambda x: x.name == LIST_RUNNING).id
        updated_card = trello_cards_service.update_card(DtoCard(id=task_card.id, idList=id_list_to))
        details = yaml.load(task_card.desc)
    else:
        log.warning("No items to process...")

    if details is not None:
        completed_order = execute_order_nike_front_end(nike_id=nike_id, details=details)

        if completed_order:
            id_list_to = QList(trello_boards_service.get_board_lists(target_board)) \
                .first(lambda x: x.name == LIST_SUCCESS).id
            trello_cards_service.update_card(DtoCard(id=updated_card.id, idList=id_list_to))
        else:
            id_list_to = QList(trello_boards_service.get_board_lists(target_board)) \
                .first(lambda x: x.name == LIST_FAILED).id
            trello_cards_service.update_card(DtoCard(id=updated_card.id, idList=id_list_to))



    """
    Send notification

    """
    #notification = CurlServicePushNotifications(notifications_id)
    #notification.send_notification("{0}")
