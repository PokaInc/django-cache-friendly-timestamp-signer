import time
import random

from datetime import timedelta
from django.core import signing
from django.utils import baseconv


class TimeFramedTimestampSigner(signing.TimestampSigner):

    def __init__(self, time_frame, uniform_distribution=True, **kwargs):
        if isinstance(time_frame, timedelta):
            self.time_frame_seconds = time_frame.total_seconds()

        elif isinstance(time_frame, int):
            self.time_frame_seconds = time_frame

        else:
            raise TypeError("time_frame must be either int(seconds) or datetime.timedelta")

        if self.time_frame_seconds < 0:
            raise ValueError("time_frame must be positive")

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
