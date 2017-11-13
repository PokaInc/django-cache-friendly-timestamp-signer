
from django.test import TestCase


class NoopTestCase(TestCase):

    def setUp(self):
        pass

    def test_noop(self):
        assert True
