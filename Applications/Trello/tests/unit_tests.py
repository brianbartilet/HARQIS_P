from Applications.Trello import *


class TestsTrello(TestCase):

    def test_view_cards(self):

        board_target = DtoBoard(
            name="Daily Dashboard Tests"
        )

        boards_api = ApiServiceBoards(source_id='Trello')
        cards_list = boards_api.get_all_open_cards_from_board(board_target)

        check = ApiServiceSearch(source_id='Trello').verify
        check.common.assert_that(len(cards_list), check.common.greater_than_or_equal_to(0))

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_add_card(self):
        board_target = DtoBoard(
            name="Daily Dashboard Tests"
        )

        list_target = DtoList(
            name="CURRENT"
        )
        cards_api = ApiServiceCards(source_id='Trello')
        boards_api = ApiServiceBoards(source_id='Trello')
        boards_list = boards_api.get_board_lists(board_target)
        card_dto = DtoCard(
            name="Card " + fake.uuid4(),
            idList=QList(boards_list).first(lambda x: x.name == list_target.name).id,
            pos='top'

        )
        card_create = cards_api.add_card(card_dto)

        check = ApiServiceCards(source_id='Trello').verify
        check.common.assert_that(len(card_create.id), check.common.greater_than(0))

        cards_api.archive_card(card_create)

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_add_card_plus_image_cover_url(self):
        board_target = DtoBoard(
            name="Daily Dashboard Tests"
        )

        list_target = DtoList(
            name="CURRENT"
        )
        cards_api = ApiServiceCards(source_id='Trello')
        boards_api = ApiServiceBoards(source_id='Trello')
        boards_list = boards_api.get_board_lists(board_target)

        card_dto = DtoCard(
            name="Card " + fake.uuid4(),
            idList=QList(boards_list).first(lambda x: x.name == list_target.name).id,
            pos='top'

        )
        card_create = cards_api.add_card(card_dto)

        check = ApiServiceCards(source_id='Trello').verify
        check.common.assert_that(len(card_create.id), check.common.greater_than(0))

        attachment_dto = DtoAttachment(setCover=True,
                                       url="https://trello-attachments.s3.amazonaws.com/56b8e0bf15387324b8ecf695/5d555e20eb376b0de7693ef9/c6746bbf62c2bb612536ee2ca1dce053/image.png")
        attachment_data = cards_api.add_attachment_to_card(card_create.id, attachment_dto)
        check.common.assert_that(len(attachment_data.id), check.common.greater_than(0))

        cards_api.archive_card(card_create)

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_get_attachments(self):

        service_trello_boards = ApiServiceBoards(source_id='Trello')
        service_trello_lists = ApiServiceLists(source_id='Trello')

        target_list = DtoList(name='JOBS')
        target_board = DtoBoard(name='Daily Dashboard Tests')

        id_list = QList(service_trello_boards.get_board_lists(target_board)) \
            .first(lambda x: x.name == target_list.name).id

        target_list.id = id_list
        current = service_trello_lists.get_all_cards_from_list(target_list)

        card = QList(current).first()

        service_trello_cards = ApiServiceCards(source_id='Trello', allow_redirects=True)
        use_attachment = QList(service_trello_cards.get_attachments(card_id=card.id)).first()
        attach = service_trello_cards.get_attachment(card_id=card.id, attachment_id=use_attachment.id)
        service_trello_cards.download_attachment(attach.url,
                                                 attach.id,
                                                 '.csv',
                                                 service_trello_cards.parameters['download_path'])

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_move_cards_pattern(self):
        move_cards_with_title_to_target_list(
            trello_id='Trello',
            board_name='Daily Dashboard Tests',
            source_list_name='PENDING',
            target_list_name='SIGNALS',
            contains_text_input='CAD'
        )

