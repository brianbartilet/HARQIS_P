from Applications.PSEITools import *


class TestsPSEI(TestCase):

    def test_accounts(self):
        service = ApiServiceStock(source_id='PSEITools')
        response = service.get_stock_price('BDO')
        assert_that(QList(response).first().symbol, equal_to('BDO'))

