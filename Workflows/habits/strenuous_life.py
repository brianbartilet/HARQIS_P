from Applications import *

str_agons_description = """
Daily Agons at 10AM 
        
```
{0}
```
"""

@app.task()
def create_trello_reminder_from_weekly_agons(
        strenuous_id,
        trello_id,
        board_name,
        list_name,
        attachment_url=None
        ):

    #  region Fetch Strenuous Data

    driver = WebDriverFactory.get_web_driver_instance(**apps_config[strenuous_id]['webdriver'])

    pl = PageStrenuousLogin(driver=driver, source_id=strenuous_id)
    pl.login(pl.parameters['username'], pl.parameters['password'])

    pa = PageAgons(driver, source_id=strenuous_id)
    agon_information = pa.get_latest_agon_info()
    pa.driver.close()

    #  endregion

    current_cards, id_list, target_board = get_board_data(trello_id, board_name, list_name)

    trello_cards_service = ApiServiceCards(trello_id)
    trello_boards_service = ApiServiceBoards(trello_id)

    #  region Add Reminders as Cards

    labels_list = ['Organization | Everyman Skills']
    labels_id_list = [l.id for l in QList(trello_boards_service.get_board_labels(target_board))
        .where(lambda x: x.name in labels_list)]

    card_dto = DtoCard(
        name="**{0}:** *{1}*[{2}]".format(agon_information.week, agon_information.name, agon_information.link),
        idList=id_list.id,
        idLabels=labels_id_list,
        pos='bottom',
        desc=str_agons_description.format(agon_information.description),

    )

    card_create = trello_cards_service.add_card(card_dto)

    if attachment_url is not None:
        attachment_dto = DtoAttachment(
            url=attachment_url,
            setCover=True
        )

        trello_cards_service.add_attachment_to_card(card_create.id, attachment_dto)

    return card_create

    #  endregion