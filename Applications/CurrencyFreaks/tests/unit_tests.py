from Applications.CurrencyFreaks.references import *

SOURCE_ID = 'CurrencyFreaks'


class TestCurrencyFreaks(TestCase):

    def test_get_latest(self):
        service = ApiServiceCurrencyFreaksRates(source_id=SOURCE_ID)
        data = service.get_latest_rates()
        assert_that(data, is_not(None))