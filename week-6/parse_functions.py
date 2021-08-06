def parse_dest(input_str):
    lookup_table = {
            "": 0,
            "M": 1,
            "D": 2,
            "MD": 3,
            "A": 4,
            "AM": 5,
            "AD": 6,
            "AMD": 7
            }
    result = lookup_table[ input_str ]
    return format(result, "03b")

def parse_jmp(input_str):
    lookup_table = {
            "": 0,
            "JGT": 1,
            "JEQ": 2,
            "JGE": 3,
            "JLT": 4,
            "JNE": 5,
            "JLE": 6,
            "JMP": 7
            }
    result = lookup_table[ input_str ]
    return format(result, "03b")

def parse_comp(input_str):
    lookup_table = {
            "": "101010", # not sure about this line
            "0": "101010",
            "1": "111111",
            "-1": "111010",
            "D": "001100",
            "A": "110000",
            "M": "110000",
            "!A": "110001",
            "!M": "110001",
            "-D": "001111",
            "-A": "110011",
            "-M": "110011",
            "D+1": "011111",
            "A+1": "110111",
            "M+1": "110111",
            "D-1": "001110",
            "A-1": "110010",
            "M-1": "110010",
            "D+A": "000010",
            "D+M": "000010",
            "D-A": "010011",
            "D-M": "010011",
            "A-D": "000111",
            "M-D": "000111",
            "D&A": "000000",
            "D&M": "000000",
            "D|A": "010101",
            "D|M": "010101"
            }
    if input_str.find("M") >= 0:
        a = 1
    else:
        a = 0
    return str(a), lookup_table[ input_str ]
