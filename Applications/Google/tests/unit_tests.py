from Applications.Google import *
from Applications.load_config import *

NODE_ID_NAME = 'GoogleAPIs'


class TestGoogleAPIs(TestCase):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def test_get_holidays(self):
        ws = ApiServiceGoogleCalendar(NODE_ID_NAME)

        data = ws.get_holidays()
        assert_that(data, is_not(None))

    @holidays_aware()
    def test_holidays_aware(self):
        log.info("Job Completed From Holidays Check")

    @pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_sheet_auth(self):
        scopes = apps_config['GoogleAPIsSheet']['parameters']['scopes']
        SERVICE = ApiServiceGoogleSheets(source_id='GoogleAPIsSheet', scopes_list=scopes)

        headers = ('ID', 'Customer Name', 'Product Code', 'Units Ordered',
                  'Unit Price', 'Status', 'Created at', 'Updated at')
        SERVICE.set_headers(headers)
        SERVICE.set_row_data([
            (1, "sexys", 'SSDSA', 2, 1.00, 'Done', '12', '2'),
            (2, "Dick", 'ZYX', 4, 2010.11, 'Done', '1', '2')
        ])

        SERVICE.update_sheet_data('A1')
        SERVICE.get_sheet_data()

    #@pytest.mark.skip(reason=SKIP_TEST_TRANSACTION)
    def test_sheet_clear(self):
        scopes = apps_config['GoogleAPIsSheet']['parameters']['scopes']
        SERVICE = ApiServiceGoogleSheets(source_id='GoogleAPIsSheet', scopes_list=scopes)
        rows = len(SERVICE.get_sheet_data('Sheet1'))
        SERVICE.clear_sheet_data(range_expression='Sheet1!1:{0}'.format(rows))




