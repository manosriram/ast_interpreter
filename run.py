from parser import Parser
from interpreter import Interpreter

source = """
 BEGIN
     BEGIN
         number := 2;
         a := number + 1;
         b := 10 * a + 10 * number / 4;
         c := a - - b
     END;
     x := 11;
 END.
"""

if __name__ == "__main__":
    p = Parser(source)
    i = Interpreter(p)
    x = i.interpret()
    print(i.GLOBAL_SCOPE)
