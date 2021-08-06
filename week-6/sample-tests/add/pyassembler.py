import argparse
from parse_functions import parse_dest, parse_comp, parse_jmp

COMMENT = "//"

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

def parser(instruct):
    instruct = instruct.replace(" ", "")
    if instruct[0] == '@':
        ins_end = instruct[1:]
        if ins_end.isnumeric():
            binary_rep = format(int(ins_end), '016b')
            return binary_rep
    else:
        dest, rest = split_two(instruct, "=")
        comp, jmp = split_two(rest, ";", reverse=True)
        dest_str = parse_dest(dest)
        a_flag, comp_str = parse_comp(comp)
        jmp_str = parse_jmp(jmp)

        assembled_str = "111" + a_flag + comp_str + dest_str + jmp_str
        assert len(assembled_str) == 16, "length of assembled instruction is " + len(assembled_str)
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

    with open(args["output"], "w") as writefile:
        for instruct_str in output:
            assembled_output = parser(instruct_str)
            writefile.write(assembled_output + "\n")
    print(output)
