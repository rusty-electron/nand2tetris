import argparse
from parse_functions import parse_dest, parse_comp, parse_jmp

COMMENT = "//"

# symbol table
# 1. remove location labels and add addresses to symbol table
# 2. add predefined symbols to symbol table
# 3. if other variable labels are used, add them to symbol table
# note: it seems that these steps could be set up as a
# preprocessing step before parsing

class SymbolTable():
    def __init__(self):
        self.symbol_table = {
                "SP": 0,
                "LCL": 1,
                "ARG": 2,
                "THIS": 3,
                "THAT": 4,
                "R0": 0,
                "R1": 1,
                "R2": 2,
                "R3": 3,
                "R4": 4,
                "R5": 5,
                "R6": 6,
                "R7": 7,
                "R8": 8,
                "R9": 9,
                "R10": 10,
                "R11": 11,
                "R12": 12,
                "R13": 13,
                "R14": 14,
                "R15": 15,
                "SCREEN": 16384,
                "KBD": 24576,
                }
        self.reg_count = 16

    def reg_increment(self):
        self.reg_count += 1

    def add(self, label, address):
        self.symbol_table[label] = address

    def first_pass(self, file_contents):
        """
        adds new location labels to the symbols table
        """
        processed = []
        counter = 0
        for instruct in file_contents:
            if instruct[0] == "(" and instruct[-1] == ")":
                # get only the label
                loc_label = instruct[1:-1]
                self.add(loc_label, counter)
            else:
                processed.append(instruct)
                counter+=1
        return processed

    def print_table(self):
        print(self.symbol_table)

def remove_inline_comment(input_str, cmt_str=COMMENT):
    comment_index = input_str.find(cmt_str)
    if comment_index > 0:
        return input_str[:comment_index].strip()
    else:
        return input_str

def preprocess(file_contents, COMMENT=COMMENT):
    split_file = file_contents.split("\n")

    # remove empty lines and comments
    stripped_file = []
    for split_str in split_file:
        strip_str = split_str.strip()
        if strip_str[:2] != COMMENT and len(strip_str) != 0:
            # remove inline comments
            split_str = remove_inline_comment(split_str)
            split_str = split_str.replace(" ", "")
            stripped_file.append(split_str)
    return stripped_file

def split_two(input_str, sep, reverse=False):
    index = input_str.find(sep)
    if index < 0:
        if not reverse:
            return '', input_str
        else:
            return input_str, ''
    else:
        return input_str[:index], input_str[index + 1:]

def parser(instruct, symbols):
    if instruct[0] == '@':
        ins_end = instruct[1:]
        if ins_end.isnumeric():
            ret_val = ins_end
        else:
            value = symbols.symbol_table.get(ins_end)
            if value is not None:
                ret_val = value
            else:
                reg_address = symbols.reg_count
                symbols.add(ins_end, reg_address)
                symbols.reg_increment()
                ret_val = reg_address
        return format(int(ret_val), "016b")
    else:
        dest, rest = split_two(instruct, "=")
        comp, jmp = split_two(rest, ";", reverse=True)
        dest_str = parse_dest(dest)
        a_flag, comp_str = parse_comp(comp)
        jmp_str = parse_jmp(jmp)

        assembled_str = "111" + a_flag + comp_str + dest_str + jmp_str
        assert len(assembled_str) == 16, "length of assembled instruction is not equal to 16 bits"
        return assembled_str

if __name__ == "__main__":
    ag = argparse.ArgumentParser()
    ag.add_argument("-f", "--asmfile", required=True, help="path to the hack asm file")
    ag.add_argument("-o", "--output", default="output.hack", help="path to the machine code output file")
    args = vars(ag.parse_args())

    with open(args["asmfile"], "r") as f:
        # read the entire file
        entire_file = f.read()

    output = preprocess(entire_file)
    symbols = SymbolTable()
    sym_output = symbols.first_pass(output)

    with open(args["output"], "w") as writefile:
        for instruct_str in sym_output:
            assembled_output = parser(instruct_str, symbols)
            writefile.write(assembled_output + "\n")
    print(output)
    symbols.print_table()
