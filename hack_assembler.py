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
        instruction_fields = {'type': 'A'}
        symbol = self.current_instruction[1:]
        if self.symbols.get_value(symbol) == 'Not exist symbol !':
            value = self.to_binary(self.next_variable_address, 15)
            self.symbols.add_symbol(symbol, value)
            self.next_variable_address += 1
            instruction_fields['value'] = value
        instruction_fields['value'] = self.symbols.get_value(symbol)
        return instruction_fields

    def handle_c_instruction(self):
        """
        Convert C-instruction into a list of dest, comp and jump.
        """
        instruction_fields = {'type': 'C'}
        # Get the jump field
        instruction_fields['jump'] = 'null'
        if self.current_instruction.count(';') == 1:
            instruction_fields['jump'] = (
                self.current_instruction.split(';')[-1])
        # Get dest and comp fields
        instruction_fields['dest'] = 'null'
        instruction_fields['comp'] = self.current_instruction.split(';')[0]
        if self.current_instruction.count('=') == 1:
            instruction_fields['dest'] = (
                self.current_instruction.split('=')[0])
            instruction_fields['comp'] = (
                self.current_instruction.split(';')[0].split('=')[1])
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


class Coder:
    """
    Convert the instructions fields from Parser class using Symbols class
    and CONSTANTS global variable into 16-bit binary instruction and
    put it in a .hack file named as the input .asm file.
    You should use generate_out_file method.
    """

    def __init__(self, symbols, parser):
        self.symbols = symbols
        self.parser = parser
        self.current_instruction = None
        self.out_file = None
        self.generate_out_file()

    def generate_out_file(self):
        """
        Convert the instructions fields from Parser class using Symbols class
        and CONSTANTS global variable into 16-bit binary instruction and
        put it in a .hack file named as the input .asm file.
        """
        # First open the out_file
        self.open_out_file()
        # Second loop through instructions and convert them to binary
        # then write them in the out_file
        for instruction in self.parser.get_instruction_fields():
            self.current_instruction = instruction
            if instruction['type'] == 'A':
                self.handle_a_instruction()
            else:
                self.handle_c_instruction()
            self.write_instruction_to_out_file()
        # Finally close the file
        self.close_out_file()

    def handle_a_instruction(self):
        """
        Convert A-instruction into 16-bit binary instruction.
        """
        self.current_instruction = '0' + self.current_instruction['value']

    def handle_c_instruction(self):
        """
        Convert C-instruction into 16-bit binary instruction.
        """
        dest = CONSTANTS['DEST'][self.current_instruction['dest']]
        jump = CONSTANTS['JUMP'][self.current_instruction['jump']]
        if self.current_instruction['comp'] in CONSTANTS['COMP0']:
            comp = CONSTANTS['COMP0'][self.current_instruction['comp']]
            a_field = '0'
        else:
            comp = CONSTANTS['COMP1'][self.current_instruction['comp']]
            a_field = '1'
        self.current_instruction = '111' + a_field + comp + dest + jump

    def write_instruction_to_out_file(self):
        """
        Write the current instruction into the out file.
        """
        self.out_file.write(self.current_instruction + '\n')

    def open_out_file(self):
        """
        Open the out_file to write the instructions to it.
        """
        # Get the input file name withoot last extension
        in_file_name = sys.argv[1].split('.')[:-1]
        in_file_name = '.'.join(in_file_name)
        # Make the out file name with new extension .hack
        out_file_name = in_file_name + '.hack'
        # Open the out_file: create a new one or overwrite an existing
        self.out_file = open(out_file_name, 'wt')

    def close_out_file(self):
        """
        Close the out_file.
        """
        # First remove the last new line
        current_file_size = self.out_file.tell()
        self.out_file.truncate(current_file_size-1)
        # Then close the file
        self.out_file.close()


if __name__ == "__main__":
    symbols_object = Symbols()
    parser_object = Parser(symbols_object)
    coder_object = Coder(symbols_object, parser_object)
    parser_object.close_in_file()
