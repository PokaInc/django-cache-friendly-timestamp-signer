import time
import random
from django.core import signing
from django.utils import baseconv


class TimeFramedTimestampSigner(signing.TimestampSigner):

    def __init__(self, time_frame_seconds, uniform_distribution=True, **kwargs):
        self.time_frame_seconds = time_frame_seconds
        self.uniform_distribution = uniform_distribution
        self._uniform_distribution_salt = None

        super(TimeFramedTimestampSigner, self).__init__(**kwargs)

    def sign(self, value):
        self._uniform_distribution_salt = hash(value)
        return super(TimeFramedTimestampSigner, self).sign(value)

    def timestamp(self):
        original = int(time.time())

        timestamp = original - (original % self.time_frame_seconds)

        if self.uniform_distribution:
            random.seed(self._uniform_distribution_salt)
            delay = random.uniform(0, self.time_frame_seconds)
            timestamp += delay

        return baseconv.base62.encode(int(timestamp))
