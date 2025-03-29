import unittest
from src.command_structure import CommandStructure

class TestCommandParser(unittest.TestCase):

    def test_command_parser(self):
        co = CommandStructure.from_string("!add 2x pizza, medium", "!", None) # type: ignore

        self.assertIsNotNone(co)
        self.assertEqual(co.command, "add") # type: ignore
        self.assertEqual(co.args_string, "2x pizza, medium") # type: ignore

        co = CommandStructure.from_string("!add", "!", None) # type: ignore
        self.assertIsNotNone(co)
        self.assertEqual(co.command, "add") # type: ignore
        self.assertEqual(co.args_string, None) # type: ignore

        co = CommandStructure.from_string("!add ", "!", None) # type: ignore
        self.assertIsNotNone(co)
        self.assertEqual(co.command, "add") # type: ignore
        self.assertEqual(co.args_string, None) # type: ignore



if __name__ == "__main__":
    unittest.main()
