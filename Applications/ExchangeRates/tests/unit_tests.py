from Applications.ExchangeRates import *
from Applications.load_config import *


class TestsRates(TestCase):

    def test_convert(self):

        service = ApiServiceTradesRates(source_id='ExchangeRates')
        values = service.get_current_rate('USD', 'PHP')

        assert_that(values, is_not(None))
