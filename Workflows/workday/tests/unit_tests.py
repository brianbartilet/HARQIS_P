from Workflows.workday import *


class UnitTests(TestCase):

    def test_punch_out(self):
        punch_in('PeonAllSec')

    def test_days_absent(self):
        check_absent_days('PeonAllSec', 'PushNotifications')

    def test_create_timesheet(self):
        create_timesheet('OracleTimesheet')

    def test_health_sheet(self):
        create_daily_health('DailyHealthForm', 'Trello', 'Daily Dashboard', 'COMPLETED')
