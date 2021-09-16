from django.test import TestCase
from app.count import add


class CountTests(TestCase):
    """Testing calculation."""

    def test_add_numbers(self):
        """Test that two numbers are added together."""
        self.assertEqual(add(3, 8), 11)
