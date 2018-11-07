# from parser import Parser
import sys
import os
from translator import Translator

TRANSLATOR = Translator()
# PARSER = Parser()
LABEL_START = "("
LABEL_END = ")"
COMMENT = '//'
A_INSTRUCTION = '@'
NULL = "null"
EQUALS = '='
JMP = ';'
BITS = 15


class SymbolTable:
    """
    A wrapper class for a dictionary of pre-defined variables.
    """
    TABLE = {}
    __R = 'R'
    __SCREEN = 16384
    __KBD = 24576
    __SP = 0
    __LCL = 1
    __ARG = 2
    __THIS = 3
    __THAT = 4

    def __init__(self):
        """
        initializes the table with all pre-defined variables.
        """
        self.__add_rs()
        self.TABLE['SCREEN'] = self.__SCREEN
        self.TABLE['KBD'] = self.__KBD
        self.TABLE['SP'] = self.__SP
        self.TABLE['LCL'] = self.__LCL
        self.TABLE['ARG'] = self.__ARG
        self.TABLE['THIS'] = self.__THIS
        self.TABLE['THAT'] = self.__THAT

    def __add_rs(self):
        for j in range(16):
            self.TABLE[self.__R + str(j)] = j


def parse_line(line):
    """The function parses a line into a list of its different parts."""
    line_b = line.split(EQUALS)
    dest = line_b[0]
    comp = NULL
    jmp = NULL
    if EQUALS in line:
        line_b = line_b[1].split(JMP)
        comp = line_b[0]
        if JMP in line:
            jmp = line_b[1]
    return [dest, comp, jmp]


def assemble_file(address):
    # initialize Symbol Table
    symbol_table = SymbolTable()
    with open(address, 'r') as f:
        # Get all lines ignoring whitespace lines or comment lines.
        lines = [line.strip() for line in f if
                 (not line.rstrip().startswith(COMMENT)
                  and len(line.strip()) != 0)]
        # Get rid of comments after instructions.
        for i in range(len(lines)):
            c = lines[i].find(COMMENT)
            if c != -1:
                lines[i] = lines[i][:c]
        # First Pass:
        first_pass(lines, symbol_table)
        # Main Pass:
        output = main_pass(lines, symbol_table)
        out_file = open(os.path.splitext(os.path.basename(address))[0] +
                        ".hack", "w+")
        out_file.write(output)
        out_file.close()


def main_pass(lines, symbol_table):
    output = ""
    n = 16
    for line in lines:
        # Line is an A-Instruction:
        if line.startswith(A_INSTRUCTION):
            # Get the value after the @
            var = line[1:]
            # Case: Var is a decimal constant
            var_to_convert = var
            # Case: Var is symbol:
            if not var.isdigit():
                if var not in symbol_table.TABLE:
                    symbol_table.TABLE[var] = n
                    n += 1
                var_to_convert = symbol_table.TABLE[var]
            output += "0" + str(bin(int(var_to_convert)))[2:].zfill(
                BITS) + "\n"
            continue
        else:  # Line is C-Instruction
            # Get rid of any whitespace in the line:
            line = ''.join(line.split())
            parts = parse_line(line)
            output += TRANSLATOR.translate_c_command(parts)
    return output


def first_pass(lines, symbol_table):
    """Loops through the file, handling only the lines with label
    declarations."""
    line_number = 0
    for line in lines:
        if line.startswith(LABEL_START):
            label = line[1:line.find(LABEL_END)]
            symbol_table[label] = line_number + 1
        else:
            line_number += 1


def validate_arg(arg):
    """Validate that the addresses received exist and if so that they are
    indeed asm files."""
    if not os.path.exists(arg):
        print("Error: Path " + arg + " doesn't exist.")
        exit(-1)
    if os.path.isfile(arg) and not arg.endswith(".asm"):
        print("Error: File " + arg + " is not an asm file.")
        exit(-1)


def main():
    # verify input files correctness:
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if os.path.isdir(arg):
            for filename in os.listdir(arg):
                if filename.endswith(".asm"):
                    assemble_file(filename)
        else:
            validate_arg(arg)
            assemble_file(arg)


if __name__ == '__main__':
    main()
