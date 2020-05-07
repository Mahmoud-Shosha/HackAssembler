"""
Tests for hack_assembler.py
"""

import unittest
import json

from hack_assembler import Symbols


class TestSymbols(unittest.TestCase):
    """
    Testing Symbols class
    """

    CONSTANTS = {}

    @classmethod
    def setUpClass(cls):
        """
        Geting the constants from constants.json
        """
        # Get the constants from constants.json
        # CONSTANTS consists of: DEST, JUMP, COMP0, COMP1, SYMBOLS
        constants_file = open('constants.json')
        constants = json.loads(constants_file.read())
        constants_file.close()

        for key, value in constants.items():
            cls.CONSTANTS[key] = value

    def setUp(self):
        """
        Initialize a class object before each test case
        """
        self.symbols = Symbols()

    def test___init__(self):
        """
        Testing the __init___ method
        """
        self.assertEqual(self.symbols.symbols, self.CONSTANTS['SYMBOLS'],
                         """
                         The Symbols object initialized with
                         a non-empty dictionary.
                         """)

    def test_add_symbol(self):
        """
        Testing the add_symbol method
        """
        # Add an existing symbol
        self.symbols.add_symbol('SCREEN', 'SCREEN_VALUE')
        # Add a non-exist symbol
        self.symbols.add_symbol('CAR', 'CAR_VALUE')
        # expected result
        result = self.CONSTANTS['SYMBOLS']
        result['CAR'] = 'CAR_VALUE'

        self.assertEqual(self.symbols.symbols, result,
                         """
                         Error while adding symbols (add_symbol) method.
                         """)

    def test_get_value(self):
        """
        Testing the get_value method
        """
        values_list = []
        # Add a new symbol and get it
        self.symbols.add_symbol('CAR', 'CAR_VALUE')
        values_list.append(self.symbols.get_value('CAR'))
        # Get a non-exist symbol
        values_list.append(self.symbols.get_value('NOT_EXIST'))
        # expected result
        result = ['CAR_VALUE', 'Not exist symbol !']

        self.assertEqual(values_list, result,
                         """
                         Error while gstting symbols (get_value) method.
                         """)


if __name__ == "__main__":
    unittest.main()
