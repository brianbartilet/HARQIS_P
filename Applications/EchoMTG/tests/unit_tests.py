from Applications.EchoMTG.references import *


class TestsEchoMTG(TestCase):

    def test_get_token(self):
        service = ApiServiceEchoMTGAuth(source_id='Tests_EchoMTG')
        response = service.get_token()
        assert_that(len(response['token']), greater_than(1))

    def test_get_collection(self):
        service = ApiServiceEchoMTGInventory(source_id='Tests_EchoMTG')
        response = service.get_collection()
        assert_that(response['message'], equal_to('Inventory list accessed.'))

    def test_get_collection_dump(self):
        service = ApiServiceEchoMTGInventory(source_id='Tests_EchoMTG')
        response = service.get_collection_dump()
        assert_that(response['status'], equal_to('success'))
        assert_that(response['showDeleted'], equal_to(True))

    def test_get_collection_lists(self):
        service = ApiServiceEchoMTGLists(source_id='Tests_EchoMTG')
        response = service.get_list_data(25878)
        assert_that(response['status'], equal_to('success'))

    def test_get_collection_dump_deleted(self):
        service = ApiServiceEchoMTGInventory(source_id='Tests_EchoMTG')
        data = QList(service.get_collection_dump()['inventoryData'])\
            .where(lambda x: x['d'] is not None)
        assert_that(len(data), greater_than_or_equal_to(0))

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_get_note(self):
        service = ApiServiceEchoMTGNotes(source_id='Tests_EchoMTG')
        data = service.get_note('62581')
        assert_that(data['message'], equal_to('note fetched'))

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_create_update_note(self):
        service = ApiServiceEchoMTGNotes(source_id='Tests_EchoMTG')
        data = service.create_note('34659557', "Test Note")
        assert_that(data['message'], equal_to('note created successfully'))
        data = service.update_note(data['note_id'], "Updated Test Note")
        assert_that(data['message'], equal_to('note created successfully'))

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_update_date_all(self):
        service = ApiServiceEchoMTGInventory(source_id='Tests_EchoMTG')
        data_test_all = QList(service.get_collection()['items'])

        for data_test in data_test_all:
            response = service.update_acquired_date(data_test['inventory_id'], '2016-01-01')
            assert_that(response['message'], equal_to('Card acquired date 2016-01-01 updated.'))

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_toggle_tradable(self):
        service = ApiServiceEchoMTGInventory(source_id='Tests_EchoMTG')
        response = service.update_toggle_tradable('34659557', True)

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_add_card(self):
        service = ApiServiceEchoMTGInventory(source_id='Tests_EchoMTG')
        mtg_card = DtoEchoMTGCard(
            mid=407657,
            foil=1

        )
        response = service.add_card_to_collection(mtg_card)

