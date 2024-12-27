import unittest
from src.utils.get_quantity_number import get_quantity_number

class TestGetQuantityNumber(unittest.TestCase):

    def test_valid_input(self):
        # Test a valid input string that should return a number and the remainder of the string
        self.assertEqual(get_quantity_number("2x pizza hawaii"), (2, "pizza hawaii"))
        self.assertEqual(get_quantity_number("10x apples"), (10, "apples"))

    def test_invalid_input(self):
        # Test an input string that doesn't match the pattern
        self.assertEqual(get_quantity_number("pizza hawaii"), (None, None))
        self.assertEqual(get_quantity_number("2 pizzas"), (None, None))
        self.assertEqual(get_quantity_number("x pizza hawaii"), (None, None))
        self.assertEqual(get_quantity_number("2x"), (None, None))

    def test_edge_cases(self):
        # Test edge cases
        self.assertEqual(get_quantity_number("0x something"), (0, "something"))
        self.assertEqual(get_quantity_number("1x "), (1, ""))
        self.assertEqual(get_quantity_number("123x items"), (123, "items"))
        self.assertEqual(get_quantity_number("2x   hawaii"), (2, "hawaii"))

    def test_empty_string(self):
        # Test an empty string input
        self.assertEqual(get_quantity_number(""), (None, None))

    def test_whitespace(self):
        # Test a string with only whitespace
        self.assertEqual(get_quantity_number("   "), (None, None))
        self.assertEqual(get_quantity_number("2x "), (2, ""))

if __name__ == "__main__":
    unittest.main()
