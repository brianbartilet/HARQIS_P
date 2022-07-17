from Applications.Google.references.web.base_api_service import *
from Applications.Google.references.dto import *
from datetime import datetime


def holidays_aware(source_id='GoogleAPIs', country_code='en.philippines'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            klass_get_holidays = ApiServiceGoogleCalendar(source_id=source_id)
            data = klass_get_holidays.get_holidays(country_code=country_code)
            today = datetime.today().strftime('%Y-%m-%d')
            exists = QList(data).where(lambda x: x['start']['date'] == today)
            if len(exists) == 0:
                return func(*args, **kwargs)
            else:
                holiday = exists.first()['summary']
                log.warning("Job skipped due to holidays in: '{0}' {1}: {2}"
                            .format(country_code, holiday, func.__name__))
        return wrapper

    return decorator


class ApiServiceGoogleCalendar(BaseApiServiceGoogle):

    def __init__(self, source_id):
        super(ApiServiceGoogleCalendar, self).__init__(source_id=source_id, client=BaseApiClient)
        self.initialize()

    def initialize(self):
        super(ApiServiceGoogleCalendar, self).initialize()
        self.request\
            .add_uri_parameter('calendar/v3/calendars')

    @deserialized(dict, child='items')
    def get_holidays(self, country_code='en.philippines'):
        self.request\
            .add_uri_parameter('{0}%23holiday%40group.v.calendar.google.com/events'.format(country_code))\
            .add_query_string('key', self.parameters['api_key'])

        response = self.send_get_request(self.request.build())

        return response
