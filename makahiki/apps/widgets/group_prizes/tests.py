"""
This file demonstrates writing tests in Makahiki. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your widget.

"""
from django.test import TransactionTestCase


class SimpleTest(TransactionTestCase):
    """simple test class."""

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
