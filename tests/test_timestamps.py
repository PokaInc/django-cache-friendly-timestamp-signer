import datetime
from freezegun import freeze_time
from django.test import TestCase

from django_cache_friendly_timestamp_signer.signer import TimeFramedTimestampSigner


class TimestampTestCase(TestCase):

    def setUp(self):
        # 30 minutes time-frames
        self.signer = TimeFramedTimestampSigner(
            time_frame=datetime.timedelta(minutes=30),
            uniform_distribution=False,
        )

    def test_signature_stays_identical_within_timeframe(self):
        with freeze_time("2017-01-01 10:00:00") as frozen_datetime:
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

            # From 10:00 to 10:29 the same signature is returned.
            assert len({sign_10_0, sign_10_10, sign_10_20, sign_10_29}) == 1

            # Trigger point at 10:30
            assert sign_10_0 != sign_10_30
            assert sign_10_0 != sign_10_40

            # Then same signature from 10:30 to 10:59
            assert sign_10_30 == sign_10_40
