COMP_INDEX = 1
DEST_INDEX = 0
JMP_INDEX = 2
M_REG = "M"
A_REG = "A"
D_REG = "D"
SR = ">>"
SL = "<<"
DEFAULT_COMP = "000000"
COMP_TABLE = {"0": "101010", "1": "111111", "-1": "111010", "D": "001100",
              "A": "110000", "!D": "001101", "!A": "110001", "-D": "001111",
              "-A": "110011", "D+1": "011111", "A+1": "110111",
              "D-1": "001110", "A-1": "110010", "D+A": "000010",
              "D-A": "010011", "A-D": "000111", "D&A": "000000",
              "D|A": "010101",
              }
DEST_TABLE = {"null": "000", "M": "001", "D": "010", "MD": "011", "A": "100",
              "AM": "101", "AD": "110", "AMD": "111"}


class Translator:
    def translate_c_command(self, parts):
        cInstruction = "1"
        comp = parts[COMP_INDEX]
        dest = parts[DEST_INDEX]
        jmp = parts[JMP_INDEX]
        cInstruction += self.__translate_comp(comp) + self.__translate_dest(
            dest) + self.__translate_jmp(jmp) + "\n"
        return cInstruction


    def __translate_comp(self, comp):
        output = ""
        c = comp
        if SR in comp or SL in comp:
            output += "01"
        else:
            output += "11"

        if M_REG in comp:
            output += "1"
            c = comp.replace(M_REG, A_REG)
        else:
            output += "0"
        if SR in c or SL in c:
            return output + self.__shift_translation(c)
        if c not in COMP_TABLE:
            print("Error: Illegal comp input: " + c)
            exit(-1)
        output += COMP_TABLE[c]
        return output

    def __shift_translation(self, comp):
        """Manually creates the binary code of the comp adn returns it"""
        output = ""
        if SR in comp:
            output += "0"
        else:
            output += "1"
        if D_REG in comp:
            output += "1"
        else:
            output += "0"
        output += "0000"
        return output

    def __translate_dest(self, dest):
        """Translates the """
        if dest not in DEST_TABLE:
            print("Error: Illegal dest input: " + dest)
            exit(-1)
        return DEST_TABLE[dest]

    def __translate_jmp(self, jmp):
        output = ["0", "0", "0"]
        if A_REG in jmp:
            output[0] = "1"
        if D_REG in jmp:
            output[1] = "1"
        if M_REG in jmp:
            output[2] = "1"
        return "".join(output)
