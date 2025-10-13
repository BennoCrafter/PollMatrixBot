import unittest
from datetime import timedelta
from src.utils.parse_time import parse_time


class TestParseTime(unittest.TestCase):
    def test_valid_times(self):
        self.assertEqual(parse_time("10s"), timedelta(seconds=10))
        self.assertEqual(parse_time("5m"), timedelta(minutes=5))
        self.assertEqual(parse_time("2h"), timedelta(hours=2))
        self.assertEqual(parse_time("3d"), timedelta(days=3))
        self.assertEqual(parse_time("1h30m"), timedelta(hours=1, minutes=30))
        self.assertEqual(
            parse_time("2h15m10s"), timedelta(hours=2, minutes=15, seconds=10)
        )
        self.assertEqual(
            parse_time("1d2h3m4s"), timedelta(days=1, hours=2, minutes=3, seconds=4)
        )
        self.assertEqual(parse_time("1d"), timedelta(days=1))
        self.assertEqual(parse_time("24h"), timedelta(hours=24))
        self.assertEqual(parse_time("60m"), timedelta(minutes=60))
        self.assertEqual(parse_time("86400s"), timedelta(seconds=86400))

    def test_case_insensitivity(self):
        self.assertEqual(parse_time("10S"), timedelta(seconds=10))
        self.assertEqual(parse_time("5M"), timedelta(minutes=5))
        self.assertEqual(parse_time("2H"), timedelta(hours=2))
        self.assertEqual(parse_time("3D"), timedelta(days=3))
        self.assertEqual(parse_time("1H30M"), timedelta(hours=1, minutes=30))

    def test_invalid_times(self):
        self.assertIsNone(parse_time("invalid"))
        self.assertIsNone(parse_time("10"))
        self.assertIsNone(parse_time("s10"))

    def test_empty_time(self):
        self.assertIsNone(parse_time(""))

    def test_zero_values(self):
        self.assertEqual(parse_time("0s"), timedelta(seconds=0))
        self.assertEqual(parse_time("0m"), timedelta(minutes=0))
        self.assertEqual(parse_time("0h"), timedelta(hours=0))
        self.assertEqual(parse_time("0d"), timedelta(days=0))
        self.assertEqual(parse_time("0d0h0m0s"), timedelta(seconds=0))
