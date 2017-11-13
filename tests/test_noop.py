
from django.test import TestCase


class NoopTestCase(TestCase):

    def setUp(self):
        pass

    def test_noop(self):
        from django_cache_friendly_timestamp_signer import noop
        assert noop() == 'noop'
