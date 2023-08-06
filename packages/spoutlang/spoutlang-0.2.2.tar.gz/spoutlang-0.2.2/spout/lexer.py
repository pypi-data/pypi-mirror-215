from enum import Enum, auto

class TokenType(Enum):
    Number = auto()
    Char = auto()
    Identifier = auto()
    String = auto()
    Let = auto()
    Const = auto()
    Fn = auto()
    Whale = auto()
    BinaryOperator = auto()
    UnaryOperator = auto()
    Equals = auto()
    Comma = auto()
    Colon = auto()
    OpenParen = auto()
    CloseParen = auto()
    Newline = auto()
    EOF = auto()

KEYWORDS = {
    "let": TokenType.Let,
    "const": TokenType.Const,
    "whale": TokenType.Whale,
    "spout": TokenType.Whale,
    "fn": TokenType.Fn
}

Logical = {
    "and": "&",
    "or": "|",
    "xor": "^",
    "lshift": ">>",
    "rshift": "<<"
}

BinOps = ["+", "-", "*", "/", "%", "&", "|", "^", "<<", ">>", "**", ","]
UnaOps = ["~"]



def Lexer(data):
    lexical = []
    #automatic newline insertion
    string = data.replace(";", "\n")
    string = string  + "\n\n"
    symbols = ["=", "+", "-", "*", "/", "%", "(", ")", "'", "&", "|", "^", "~", "!", "<", ">", "\n",",", ":", "<<", ">>", "**"]

    lexed = []
    temp = ""
    skipline = False
    
    i = 0
    while (i < len(string)):
        char = string[i]
        if skipline and char == "\n":
            skipline = False
        if skipline:
            i+=1
            continue
        if char != " " and char != "\t":
            temp += char
        if (i+1 < len(string)):
            if temp == "/" and string[i+1] == "/":
                lexed.append("<comment>")
                temp = ""
                skipline = True
            # handle strings
            if char == "\"":
                while(string[i+1] != "\""):
                    i+=1
                    temp += string[i]
                    if i >= len(string):
                        raise f"Unmatched double quotes (\") at {i}"
                temp+="\""
                i+=1
                lexed.append(temp)
                temp=""
                if i+1 == len(string):
                    continue
            if char == "'":
                while(string[i+1] != "'"):
                    i+=1
                    temp += string[i]
                    if i >= len(string):
                        raise f"Unmatched single quotes (\') at {i}"
                temp+="'"
                i+=1
                lexed.append(temp)
                temp=""
                if i+1 == len(string):
                    continue
            
            # Handle double symbols
            if char == "<" and string[i+1] == "<":
                temp += string[i+1]
                i+=1
            if char == ">" and string[i+1] == ">":
                temp += string[i+1]
                i+=1
            if char == "*" and string[i+1] == "*":
                temp += string[i+1]
                i+=1
            
            
            if string[i+1] == " " or string[i+1] == "\t" or string[i+1] in symbols or temp in symbols:
                if temp == "\n":
                    temp = "<newline>"
                if temp != "":
                    lexed.append(temp)  
                temp = ""
        i+=1
        
        # if temp != "":
        #     if temp == "\n": lexed.append("<newline>")
        #     else: lexed.append(temp)
    # print(lexed)
    tokens = tokenize(lexed)
    return tokens

def parseInt(value):
    last = ""
    base = 10
    if len(value)>2 and value[0] == "0" and value[1].isalpha():
        last = value[2:]
        if value[1] == 'b':
            base = 2
        elif value[1] == 'o':
            base = 8
        elif value[1] == 'x':
            base = 16
            last = str(int(last, base))
    else:
        last = value
    
    if last.isnumeric():
        return {"value": int(last, base), "base": base}
    return False
    

def token(value, type):
    return {"value": value, "type": type}

def tokenize(lex):
    tokens = []

    while(len(lex)):
        if lex[0] == "(":
            tokens.append(token(lex.pop(0),TokenType.OpenParen))
        elif lex[0] == ")":
            tokens.append(token(lex.pop(0),TokenType.CloseParen))
        elif lex[0] == ",":
            tokens.append(token(lex.pop(0),TokenType.Comma))
        elif lex[0] == ":":
            tokens.append(token(lex.pop(0),TokenType.Colon))
        elif lex[0] in BinOps:
            tokens.append(token(lex.pop(0),TokenType.BinaryOperator))
        elif lex[0] == "=":
            tokens.append(token(lex.pop(0),TokenType.Equals))
        elif lex[0] == "<comment>":
            lex.pop(0)
        elif lex[0] == "<newline>":
            tokens.append(token(lex.pop(0),TokenType.Newline))
        else:
            if parseInt(lex[0]):
                tokens.append(token(lex.pop(0), TokenType.Number))

            else:
                reserved = lex[0] in KEYWORDS
                if reserved:
                    tokens.append(token(lex[0], KEYWORDS[lex.pop(0)]))
                elif lex[0][0] == "\"":
                    tokens.append(token(lex.pop(0)[1:-1], TokenType.String))
                elif lex[0][0] == "'":
                    tokens.append(token(lex.pop(0), TokenType.Char))
                elif lex[0] in Logical:
                    tokens.append(token(Logical[lex.pop(0)], TokenType.BinaryOperator))
                else:
                    tokens.append(token(lex.pop(0), TokenType.Identifier))
            

    tokens.append(token("EndOfFile", TokenType.EOF))
    return tokens
            


        










