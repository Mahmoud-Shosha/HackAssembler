# Hack Assembler

An assembler for Hack computer in python programming langauge.

## Installation

- [Download python3.6](https://www.python.org/downloads/)
- Install dependencies  
`sudo apt-get install python3-pip`   
`pip3 install virtualenv`  
`virtualenv -p python3 venv`  
`source venv/bin/activate`  
`pip3 install -r requirements.txt`  
- Download the repository

## Getting started

 - You pass the hack_assembler.py the .asm file (Hack computer assembly code) to get the .hack file (Hack computer binary machine code)  
`python <path to hack_assembler.py> < path to .asm file>`  
Example: `python hack_assembler.py Pong.asm`  
After running the command you will get the .hack file in the same directory of the .asm file.  

## Program Structure
The program has the classes  
- Symbols : Keeps track of all (labels and variables) memory locations.  
Interface:
```python
    def add_symbol(self, symbol, value):
        """
        If the symbol is not in self.symbols, then add it.
        """
        ...

    def get_value(self, symbol):
        """
        Return the value of the passed symbol from self.symbols
        """
        ...
```
- Parser : Reads the .asm file and puts (labels and variables) memory locations in Symbols object and returns the instructions as instructions fields.  
Interface:
```python
    def get_instruction_fields(self):
        """
        Get an instruction fields at a time.
        the same as get_instruction method but all symbols
        are converted to numbers and returns a list of instruction fields.
        """
        ...

    def close_in_file(self):
        """
        Close the in_file to save resources.
        """
        ...
```
- Coder : Convert the instructions fields from Parser class using Symbols class and CONSTANTS global variable into 16-bit binary instruction and  
  put it in a .hack file named as the input .asm file.  
  Interface:
  ```python
      def generate_out_file(self):
          """
          Convert the instructions fields from Parser class using Symbols class
          and CONSTANTS global variable into 16-bit binary instruction and
          put it in a .hack file named as the input .asm file.
          """
          ...
  ```
