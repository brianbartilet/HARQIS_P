from Applications.TwelveDataTrading.references import *


class TestsTwelveDataTrading(TestCase):

    def test_get_all_available_indicators(self):
        service = ApiTechnicalIndicators(source_id='TwelveTrading')
        data = service.get_all_indicators()
        assert_that(len(data), greater_than_or_equal_to(1))

    def test_get_indicator_data(self):
        service = ApiIndicatorsFeed(source_id='TwelveTrading', indicator_short_name='ATR')

        dto = IndicatorParameters(
            symbol='EUR/USD',
            interval=EnumTimeframe.H1.value
        )
        data = service.get_indicator_values(dto)
        assert_that(len(data), greater_than_or_equal_to(1))
