import sys
import json
from spout.parser import Parser
from spout.interpreter import Interpreter
from spout.spout import Runtime

def main():
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        data = ""
        with open(filename, 'r') as f:
            data = f.read()
        if len(sys.argv) >= 3 and sys.argv[2] == "--ast":
            ast = Runtime().AST(data)
            print(json.dumps(ast, indent=2))
        else:
            Runtime().run(data)
            
    else:
        parser = Parser()
        interpreter = Interpreter()
        print(f"\033[36mSpout\033[0m REPL v0.2")
        src = ""
        while True:
            data = input(">>> ") + "\n"
            if data == "exit\n":
                break
            elif data[-2:] == ";\n":
                src += data[:-1]
            else:
                src += data
                ast = parser.createAST(src)
                out = interpreter.eval_program(ast)
                src = ""
                if out == "undefined": print(f"\033[90mundefined\033[0m ") # 90m  is grey text
                else: 
                    if not isinstance(out, dict): print(out)
                    else: print(out["value"]) 
                
        

           


if __name__ == "__main__":
    main()
