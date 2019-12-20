from django.test import TestCase

from app.calc import sum


class CalcTests(TestCase):

    def test_sum(self):
        """Test a sum"""
        result = sum(3, 8)
        self.assertEqual(result, 11)
