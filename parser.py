NULL = "null"

EQUALS = '='
JMP = ';'


class Parser:
    def parse_line(self, line):
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
