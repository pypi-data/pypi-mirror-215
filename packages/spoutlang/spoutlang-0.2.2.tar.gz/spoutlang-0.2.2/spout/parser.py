from .lexer import TokenType, Lexer, parseInt
from .environment import defineUndefined

class Parser:
    # have a private token list
    def __init__(self):
        self.tokens = []

    def notEOF(self):
        return self.tokens[0]["type"] != TokenType.EOF
    
    def consume(self):
        popped = self.tokens.pop(0)
        return popped
    
    def terminate_newline(self):
        while self.peek()["type"]==TokenType.Newline:
            self.consume()

    def peek(self):
        return self.tokens[0]

    def expect(self, type):
        if self.peek()["type"] == type:
            return self.consume()
        else:
            raise Exception("Expected " + type + " but got " + self.peek()["type"][0])

    def createAST(self, sourceCode):
        self.tokens = Lexer(sourceCode)
        ast = {
            "type": "Program",
            "body": []
        }
        while(self.notEOF()):
            ast["body"].append(self.parse_stmt())
        
        return ast

    def parse_stmt(self):
        ttype = self.peek()["type"]
        if ttype == TokenType.Let or ttype == TokenType.Const:
            return self.parse_var_declaration()
        elif ttype == TokenType.Fn:
            return self.parse_fn_declaration()
        elif ttype == TokenType.Whale:
            return self.parse_whale()
        return self.parse_expr()

    def parse_var_declaration(self):
        isConst = self.consume()["type"] == TokenType.Const
        name = self.expect(TokenType.Identifier)["value"]
        if self.peek()["type"] == TokenType.Newline:
            self.consume()
            if isConst:
                raise Exception("Constant values must have value at declaration")
            return {
                "type" : "VariableDeclaration",
                "name" : name,
                "const": False,
                "value": defineUndefined()
            }
        self.expect(TokenType.Equals)
        value = self.parse_expr()
        dec =  {
            "type": "VariableDeclaration",
            "name": name,
            "value": value,
            "const": isConst
        }
        self.expect(TokenType.Newline)
        return dec

    def parse_fn_declaration(self):
        self.consume()
        name = self.expect(TokenType.Identifier)["value"]
        arg = []
        if self.peek()["type"] == TokenType.OpenParen:
            self.consume()
            self.terminate_newline()
            while self.peek()["type"] != TokenType.CloseParen:
                arg.append(self.parse_expr())
                if self.peek()["type"] == TokenType.Comma:
                    self.consume()
                self.terminate_newline()
            self.expect(TokenType.CloseParen)
        else:
            while self.peek()["type"] != TokenType.Colon:
                arg.append(self.parse_expr())
                if self.peek()["type"] == TokenType.Comma:
                    self.consume()
        self.expect(TokenType.Colon)
        # Check if everything is an Identifier
        params = []
        for i in arg:
            if i["type"] != "Identifier":
                raise Exception("Function parameters must be identifiers")
            params.append(i["value"])

        body = []
        self.terminate_newline()
        if self.peek()["type"] == TokenType.OpenParen:
            self.consume()
            while(self.peek()["type"] != TokenType.EOF and self.peek()["type"] != TokenType.CloseParen):
                body.append(self.parse_stmt())
            self.expect(TokenType.CloseParen)
        else: 
            while(self.peek()["type"] != TokenType.EOF and self.peek()["type"] != TokenType.Newline):
                body.append(self.parse_stmt())
            
        return {
            "type": "FunctionDeclaration",
            "name": name,
            "parameters": params,
            "body": body
        }
        


    def parse_whale(self):
        self.consume()
        return {
            "type": "WhalingExpression",
            "value": self.parse_stmt()
            }

    def parse_expr(self):
        return self.parse_assignment_expr()
    
    def parse_assignment_expr(self):
        left = self.parse_bitwise_expr()
        if self.peek()["type"] == TokenType.Equals:
            self.consume()
            right = self.parse_bitwise_expr()
            return {
                "type": "AssignmentExpression",
                "left": left,
                "right": right
            }
        return left

    def parse_bitwise_expr(self):
        left = self.parse_shift_expr()
        while self.peek()["value"] == "&" or self.peek()["value"] == "|" or self.peek()["value"] == "^":
            op = self.consume()
            right = self.parse_shift_expr()
            left = {
                "type": "BinaryExpression",
                "operator": op["value"],
                "left": left,
                "right": right
            }
        return left

    def parse_shift_expr(self):
        left = self.parse_additive_expr()
        while self.peek()["value"] == "<<" or self.peek()["value"] == ">>":
            op = self.consume()
            right = self.parse_additive_expr()
            left = {
                "type": "BinaryExpression",
                "operator": op["value"],
                "left": left,
                "right": right
            }
        return left

    def parse_additive_expr(self):
        left = self.parse_multiplicative_expr()
        while self.peek()["value"] == "+" or self.peek()["value"] == "-":
            op = self.consume()
            right = self.parse_multiplicative_expr()
            left = {
                "type": "BinaryExpression",
                "operator": op["value"],
                "left": left,
                "right": right
            }
        return left
    
    def parse_multiplicative_expr(self):
        left = self.parse_exponential_expr()
        while self.peek()["value"] == "*" or self.peek()["value"] == "/" or self.peek()["value"] == "%":
            op = self.consume()
            right = self.parse_exponential_expr()
            left = {
                "type": "BinaryExpression",
                "operator": op["value"],
                "left": left,
                "right": right
            }
        return left
    
    def parse_exponential_expr(self):
        left = self.parse_call_member_expr()
        while self.peek()["value"] == "**":
            op = self.consume()
            right = self.parse_call_member_expr()
            left = {
                "type": "BinaryExpression",
                "operator": op["value"],
                "left": left,
                "right": right
            }
        return left

    def parse_call_member_expr(self):
        caller = self.parse_primary_expr()
        if self.peek()["type"] == TokenType.OpenParen:
            return self.parse_call_expr(caller)
        return caller

    def parse_call_expr(self, callee):
        call_expr = {
            "type": "CallExpression",
            "callee": callee,
            "args": self.parse_args()
        }
        if self.peek()["type"] == TokenType.OpenParen:
            call_expr = self.parse_call_expr(call_expr)
        return call_expr

    def parse_args(self):
        self.expect(TokenType.OpenParen)
        args = []
        while self.peek()["type"] != TokenType.CloseParen:
            args.append(self.parse_expr())
            if self.peek()["type"] == TokenType.Comma:
                self.consume()
        self.expect(TokenType.CloseParen)
        return args

    def parse_primary_expr(self):
        curr = self.peek()["type"]
        if curr == TokenType.Number:
            num = parseInt(self.consume()["value"])
            return {
                "type": "NumericLiteral",
                "value": num["value"],
                "base": num["base"],
                "dtype": "int"
            }
        elif curr == TokenType.String:
            return {
                "type": "StringLiteral",
                "value": self.consume()["value"],
                "dtype": "string"
            }
        elif curr == TokenType.Identifier:
            return {
                "type": "Identifier",
                "value": self.consume()["value"]
            }
        elif curr == TokenType.OpenParen:
            self.consume()
            expr = self.parse_expr()
            self.expect(TokenType.CloseParen)
            return expr
        elif curr == TokenType.Newline:
            self.consume()
            return
        elif curr == TokenType.EOF:
            print("what?")
        else:
            raise Exception("Unexpected token " + self.peek()["value"])
        





        
