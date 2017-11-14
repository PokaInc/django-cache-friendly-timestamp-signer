import datetime

from django.core.signing import Signer
from django.utils import baseconv
from freezegun import freeze_time
from django.test import TestCase

from django_cache_friendly_timestamp_signer.signer import TimeFramedTimestampSigner


class UniformDistributionTestCase(TestCase):

    def setUp(self):
        # 30 minutes time-frames
        self.signer = TimeFramedTimestampSigner(
            time_frame=datetime.timedelta(minutes=30),
            uniform_distribution=True,
        )
        self.base_signer = Signer(salt=self.signer.salt)

    def _extract_timestamp(self, signed_value):
        unsigned = self.base_signer.unsign(signed_value)
        _, timestamp = unsigned.rsplit(self.signer.sep, 1)
        return baseconv.base62.decode(timestamp)

    def _extract_base_delta(self, signed_value):
        timestamp = self._extract_timestamp(signed_value)
        delta = timestamp % self.signer.time_frame_seconds
        return delta

    def test_signature_delay_always_the_same_across_time_frames(self):
        with freeze_time(datetime.datetime.now()) as frozen_datetime:
            sign_1 = self.signer.sign("test")
            delta_1 = self._extract_base_delta(sign_1)

            frozen_datetime.tick(delta=datetime.timedelta(seconds=self.signer.time_frame_seconds))

            sign_2 = self.signer.sign("test")
            delta_2 = self._extract_base_delta(sign_2)

            frozen_datetime.tick(delta=datetime.timedelta(seconds=self.signer.time_frame_seconds))

            sign_3 = self.signer.sign("test")
            delta_3 = self._extract_base_delta(sign_3)

            # 3 different signatures
            assert len({sign_1, sign_2, sign_3}) == 3

            # Delta always the same across time frames
            assert len({delta_1, delta_2, delta_3}) == 1

    def test_timestamp_changes_per_value(self):
        with freeze_time(datetime.datetime.now()):
            sign_a = self.signer.sign("test_A")
            sign_b = self.signer.sign("test_B")
            sign_c = self.signer.sign("test_C")

            timestamp_a = self._extract_timestamp(sign_a)
            timestamp_b = self._extract_timestamp(sign_b)
            timestamp_c = self._extract_timestamp(sign_c)

            # All different
            assert len({timestamp_a, timestamp_b, timestamp_c}) == 3
