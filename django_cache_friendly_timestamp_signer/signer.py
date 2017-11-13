import time
from django.core import signing
from django.utils import baseconv


class TimeFramedTimestampSigner(signing.TimestampSigner):

    def __init__(self, time_frame_seconds, salt=None, **kwargs):
        if salt is not None:
            assert isinstance(salt, str), "Salt must be string-like"

        self.time_frame_seconds = time_frame_seconds
        self.salt = salt

        super(TimeFramedTimestampSigner, self).__init__(**kwargs)

    def timestamp(self):
        original = int(time.time())

        floored = original - (original % self.time_frame_seconds)

        return baseconv.base62.encode(floored)
