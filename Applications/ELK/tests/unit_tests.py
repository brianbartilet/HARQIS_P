from Applications.ELK import *
from Workflows import INDEX_ROOT_NAME_SCREENER
from Applications.Investagrams.references.dto import *


class TestData(JsonObject):
    blur = None
    borg = None


class TestsELK(TestCase):

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_post_data(self):
        json_dump = TestData(borg="wushu", blur="Test")
        send_json_data_to_elastic_server(json_dump.get_dict(), 'test_index_hello_world', 'test')

    def test_get_data(self):
        index_name = '{0}'.format(INDEX_ROOT_NAME_SCREENER).lower()

        data = get_index_data_from_elastic(index_name=index_name,
                                    app_config_name='ElasticSearch',
                                    type_hook=DtoStockInvestagrams)
        assert_that(len(data), greater_than_or_equal_to(0))

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    @elastic_logging()
    def test_decorator_another(self, test: str, param):
        raise Exception

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    @elastic_logging()
    def test_decorator_another_pass(self, test: str, param):
        pass

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_runner(self):
        self.test_decorator_another("HELLO", "WORLD")

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_pass(self):
        self.test_decorator_another_pass("HELLO", "WORLD")

