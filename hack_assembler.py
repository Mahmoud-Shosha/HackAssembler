"""
An assembler for Hack computer.
"""

import sys
import json


# Get the constants from constants.json
# CONSTANTS consists of: DEST, JUMP, COMP0, COMP1, SYMBOLS
CONSTANTS_FILE = open('constants.json')
CONSTANTS = json.loads(CONSTANTS_FILE.read())
CONSTANTS_FILE.close()


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


class Parser:
    """
    A class for parsing the input file (.asm) into
    a commands consisting of a list of fields.
    Use get_instruction_fields method to get an instruction.
    After ending, remember to call close_in_file method.
    """

    def __init__(self, symbols):
        self.symbols = symbols
        self.in_file = open(sys.argv[1])
        # Hack language specifications: variables are put in memory
        # locations starting from 16
        self.next_variable_address = 16
        self.current_instruction = None
        self.add_labels()

    def add_labels(self):
        """
        Add all labels in the Symbols object.
        (first pass)
        """
        next_instruction = 0
        for code in self.get_code_line():
            # Checking for label declarations
            if code[0] == '(':
                symbol = code[1:-1]
                value = self.to_binary(next_instruction, 15)
                self.symbols.add_symbol(symbol, value)
            else:
                next_instruction += 1

    def get_instruction_fields(self):
        """
        Get an instruction fields at a time.
        the same as get_instruction method but all symbols
        are converted to numbers and returns a list of instruction fields.
        """
        for instruction in self.get_instruction():
            self.current_instruction = instruction
            if instruction[0] == '@':
                yield self.handle_a_instruction()
            else:
                yield self.handle_c_instruction()

    def handle_a_instruction(self):
        """
        Convert A-instruction into a list of '@' and value.
        This includes convert any symbol to value and
        add new variables to self.symbols object.
        """
        symbol = self.current_instruction[1:]
        if self.symbols.get_value(symbol) == 'Not exist symbol !':
            value = self.to_binary(self.next_variable_address, 15)
            self.symbols.add_symbol(symbol, value)
            self.next_variable_address += 1
            return ['@', value]
        return ['@', self.symbols.get_value(symbol)]

    def handle_c_instruction(self):
        """
        Convert C-instruction into a list of dest, comp and jump.
        """
        # Get the jump field as the second item in the list instruction_fields
        instruction_fields = self.current_instruction.split(';')
        # Get dest and comp fields
        new_fields = instruction_fields[0].split('=')
        # replace the first item in instruction_fields with dest and cpmp
        if len(new_fields) == 2:
            instruction_fields.pop(0)
            instruction_fields.insert(0, new_fields[1])
            instruction_fields.insert(0, new_fields[0])
        return instruction_fields

    def get_instruction(self):
        """
        Get an instruction at a time.
        The same as get_code_line but without label declarations.
        """
        for instruction in self.get_code_line():
            if instruction[0] != '(':
                yield instruction

    def get_code_line(self):
        """
        Get a line of code at a time.
        The .asm file but no comments and whitespace.
        """
        for line in self.in_file:
            # removing comments the whitespace
            if line.count('//') != 0:
                line = line[0:line.find('//')]
            code = line.strip()
            # filtering empty lines
            if code != '':
                yield code
        # Return to the beginning of the file for later uses
        self.in_file.seek(0)

    def close_in_file(self):
        """
        Close the in_file to save resources.
        """
        self.in_file.close()

    @staticmethod
    def to_binary(decimal_number, digit_numbers):
        """
        Convert the decimal_number into a binary number of digit_numbers bits.
        """
        binary = bin(decimal_number)[2:]
        while len(binary) < digit_numbers:
            binary = '0' + binary
        return binary
