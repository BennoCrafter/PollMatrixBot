import unittest
from src.utils.insert_invisible_char import insert_invisible_char

class TestInsertInvisibleChar(unittest.TestCase):

    def test_valid_input(self):
        name = "Benno"
        self.assertNotEqual(insert_invisible_char(name), name)

    def test_empty_string(self):
        self.assertNotEqual(insert_invisible_char(""), "")

if __name__ == "__main__":
    unittest.main()
