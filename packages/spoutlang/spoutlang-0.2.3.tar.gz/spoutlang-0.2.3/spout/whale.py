
OPS = {
    "+": "ADD",
    "-": "SUB",
    "*": "MULT",
    "/": "DIV",
    "**": "POW",
    "&": "AND",
    "|": "OR",
    "^": "XOR",
    "<<": "LSHIFT",
    ">>": "RSHIFT",
    "%": "MOD"
}
KWORDS ={
    "ADD": "+",
    "SUB": "-",
    "MULT": "*",
    "DIV": "/",
    "POW": "**",
    "AND": "&",
    "OR": "|",
    "XOR": "^",
    "LSHIFT": "<<",
    "RSHIFT": ">>",
    "MOD": "%"
}

def render(operator: str, result: int, var1: int, var2: int ):
    char, word = "", ""
    if operator in OPS:
        char = operator
        word = OPS[operator]
    else:
        word = operator.upper()
        char = KWORDS[word]
    operation, v_len= operation_builder(char, word)

    length = max(result.bit_length(), var1.bit_length(), var2.bit_length())
    form = "{0:0" + f"{length}"+ "b}"
    pad = " "* v_len
    result = pad + form.format(result) + f"={result}"
    var1 = pad + form.format(var1) + f"={var1}"
    var2 = operation + form.format(var2) + f"={var2}"
    strike = "-"* len(var1)
    print(var1, var2, strike, result, "\n", sep="\n")




def operation_builder(char, word):
    # visual_length= len(f"{word} {char} ")
    visual_length = 10
    op_str = f"\033[36m{word} {char}\033[0m " + " " * (visual_length - len(f"{word} {char} "))
    return (op_str,visual_length)

