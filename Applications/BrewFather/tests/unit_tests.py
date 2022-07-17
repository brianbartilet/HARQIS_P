from Applications.BrewFather.references import *

SOURCE_ID = 'BrewFather'


class TestsBrewFather(TestCase):

    def test_batch_data(self):
        service = ApiServiceBrewFatherBatches(source_id=SOURCE_ID)
        data = service.get_batches()
        assert_that(data, is_not(None))

        batch_target = QList(data).first()
        id = batch_target['_id']

        batch_data = service.get_batch_information(id)
        assert(batch_data, is_not(None))

        batch_reading = service.get_batch_readings(id)
        assert (batch_reading, is_not(None))

        batch_reading_last = service.get_batch_last_reading(id)
        assert (batch_reading_last, is_not(None))

        batch_tracker = service.get_batch_brewtracker(id)
        assert (batch_tracker, is_not(None))