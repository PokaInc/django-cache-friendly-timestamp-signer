import datetime

from django.test import TestCase

from django_cache_friendly_timestamp_signer.signer import TimeFramedTimestampSigner


class ConfigurationTestCase(TestCase):

    def test_allow_timedelta(self):
        signer = TimeFramedTimestampSigner(datetime.timedelta(hours=3))
        assert signer.time_frame_seconds == 10800

        signer = TimeFramedTimestampSigner(datetime.timedelta(minutes=1))
        assert signer.time_frame_seconds == 60

        signer = TimeFramedTimestampSigner(datetime.timedelta(seconds=1))
        assert signer.time_frame_seconds == 1

    def test_allow_integer(self):
        signer = TimeFramedTimestampSigner(10)
        assert signer.time_frame_seconds == 10

    def test_raise_on_invalid_time_frame(self):
        with self.assertRaises(AssertionError):
            TimeFramedTimestampSigner("test")

        with self.assertRaises(AssertionError):
            # Can't work with float in base62
            TimeFramedTimestampSigner(30.25)

        with self.assertRaises(AssertionError):
            TimeFramedTimestampSigner(-100)

        with self.assertRaises(AssertionError):
            TimeFramedTimestampSigner(datetime.timedelta(days=-5))
