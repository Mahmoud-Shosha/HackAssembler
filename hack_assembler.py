"""
An assembler for Hack computer.
"""

import json


if __name__ == "__main__":
    # Get the constants from constants.json
    # CONSTANTS consists of: DEST, JUMP, COMP0, COMP1, SYMBOLS
    CONSTANTS = open('constants.json')
    CONSTANTS = json.loads(CONSTANTS.read())
