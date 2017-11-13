import datetime
from freezegun import freeze_time
from django.test import TestCase

from django_cache_friendly_timestamp_signer.signer import TimeFramedTimestampSigner


class TimestampTestCase(TestCase):

    def setUp(self):
        # 30 minutes time-frames
        self.signer = TimeFramedTimestampSigner(time_frame_seconds=1800, uniform_distribution=False)

    def test_signature_stays_identical_within_timeframe(self):
        initial_datetime = datetime.datetime(
            year=2017,
            month=1,
            day=1,
            hour=10,
            minute=0,
            second=0
        )  # 10:00:00

        with freeze_time(initial_datetime) as frozen_datetime:
            sign_10_0 = self.signer.sign("test")

            frozen_datetime.tick(delta=datetime.timedelta(minutes=10))
            sign_10_10 = self.signer.sign("test")

            frozen_datetime.tick(delta=datetime.timedelta(minutes=10))
            sign_10_20 = self.signer.sign("test")

            frozen_datetime.tick(delta=datetime.timedelta(minutes=9))
            sign_10_29 = self.signer.sign("test")

            frozen_datetime.tick(delta=datetime.timedelta(minutes=1))
            sign_10_30 = self.signer.sign("test")

            frozen_datetime.tick(delta=datetime.timedelta(minutes=10))
            sign_10_40 = self.signer.sign("test")

            assert sign_10_0 == sign_10_10
            assert sign_10_0 == sign_10_20
            assert sign_10_0 == sign_10_29

            assert sign_10_0 != sign_10_30
            assert sign_10_0 != sign_10_40

            assert sign_10_30 == sign_10_40
