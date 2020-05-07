"""
An assembler for Hack computer.
"""

import json


class Symbols:
    """
    A class for keeping track of all symbols and their values.
    """

    def __init__(self):
        self.symbols = {}
        self.__init_symbols()

    def __init_symbols(self):
        """
        Initialize the symbols by addding constant symbols in it.
        """
        for key, value in CONSTANTS['SYMBOLS'].items():
            self.symbols[key] = value

    def add_symbol(self, symbol, value):
        """
        If the symbol is not in self.symbols, then add it.
        """
        if symbol not in self.symbols:
            self.symbols[symbol] = value

    def get_value(self, symbol):
        """
        Return the value of the passed symbol from self.symbols
        """
        if symbol in self.symbols:
            return self.symbols[symbol]
        return 'Not exist symbol !'


if __name__ == "__main__":
    # Get the constants from constants.json
    # CONSTANTS consists of: DEST, JUMP, COMP0, COMP1, SYMBOLS
    CONSTANTS = open('constants.json')
    CONSTANTS = json.loads(CONSTANTS.read())
