from Applications.OANDA.references import *

SOURCE_ID = 'Tests_OANDA'


class TestsOANDA(TestCase):

    def test_accounts_data(self):
        service = ApiServiceAccount(source_id=SOURCE_ID)
        data = service.get_account_info()
        assert_that(data, is_not(None))

    def test_auto_chartist(self):
        service = ApiServiceAutoChartist(source_id=SOURCE_ID)
        data = service.get_signals()
        assert_that(len(data), greater_than_or_equal_to(0))

    def test_get_open_trades(self):
        service = ApiServiceAccount(source_id=SOURCE_ID)
        data = service.get_account_info()

        id = QList(data.accounts).first().id

        service_trades = ApiServiceTrades(source_id=SOURCE_ID)
        data = service_trades.get_trades_from_account(id)
        assert_that(len(data), greater_than_or_equal_to(0))

    def test_pricing(self):
        service = ApiServiceAccount(source_id=SOURCE_ID)
        data = service.get_account_info()

        id = QList(data.accounts).first().id

        service_price = ApiServicePricing(source_id=SOURCE_ID)
        data = service_price.get_pricing(id, 'AUD_USD')

        assert_that(len(data), greater_than_or_equal_to(1))

    def test_get_orders(self):
        service = ApiServiceAccount(source_id=SOURCE_ID)
        data = service.get_account_info()

        id = QList(data.accounts).first().id

        service = ApiServiceOrders(source_id=SOURCE_ID)
        data = service.get_orders(id)

        assert_that(len(data['orders']), greater_than_or_equal_to(0))

    def test_account_instrument(self):
        service = ApiServiceAccount(source_id=SOURCE_ID)
        data = service.get_account_info()
        id_account = QList(data.accounts).first().id

        data = service.get_account_instrument_details(account_id=id_account)
        assert_that(len(data), greater_than_or_equal_to(1))
        data = service.get_account_instrument_details(account_id=id_account, currency_name='EUR_USD')
        assert_that(len(data), equal_to(1))

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_create_market_order(self):
        service = ApiServiceAccount(source_id=SOURCE_ID)
        data = service.get_account_info()

        id = QList(data.accounts).first().id

        dto = DtoOrder(
            order=DtoMarketOrderRequest(
                instrument='EUR_USD',
                positionFill=EnumOrderPositionFill.DEFAULT.value,
                timeInForce=EnumTimeInForce.FOK.value,
                units='100',
                type=EnumOrderType.MARKET.value,
            )
        )
        service = ApiServiceOrders(source_id=SOURCE_ID)
        service_trades = ApiServiceTrades(source_id=SOURCE_ID)
        pre_trades = service_trades.get_trades_from_account(id)

        service.create_order(id, dto)

        post_trades = service_trades.get_trades_from_account(id)

        assert_that(len(pre_trades) + 1, equal_to(len(post_trades)))

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_create_limit_order(self):
        service = ApiServiceAccount(source_id=SOURCE_ID)
        data = service.get_account_info()

        id = QList(data.accounts).first().id

        dto = DtoOrder(
            order=DtoLimitOrderRequest(
                price="1.16",
                #stopLossOnFill=DtoStopLossDetails(price="1.19", timeInForce=EnumTimeInForce.GTC.value),
                #takeProfitOnFill=DtoTakeProfitDetails(price='1.16200'),
                timeInForce=EnumTimeInForce.GTC.value,
                instrument='EUR_USD',
                units='1000', #-/_
                type=EnumOrderType.LIMIT.value,
                positionFill=EnumOrderPositionFill.DEFAULT.value,
            )
        )
        service = ApiServiceOrders(source_id=SOURCE_ID)
        service_orders = ApiServiceOrders(source_id=SOURCE_ID)
        pre_orders = service_orders.get_orders(id)

        data = service.create_order(id, dto)

        post_orders = service_orders.get_orders(id)

        assert_that(len(pre_orders.orders) + 1, equal_to(len(post_orders.orders)))

