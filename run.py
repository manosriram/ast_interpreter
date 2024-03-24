from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

source = """
 PROGRAM test;
 VAR
    a : INTEGER;
    b, c : REAL;

 BEGIN
     BEGIN
         number := 2;
         a := 100;
         b := 2.22;
         c := 1.12;
         name := 'mano';
         num_plus_one := NUMBER + 1;
         calculation := 10 * a + 10 * number DIV 4;
         number_equals := number == 3;
         number_not_equals := number != 3;
         nested_operations := a - - number;
         real_div := b / c;
         int_div := b DIV c;
         { this is a comment }
         {
            this is a comment block
         }
     END
 END.
"""

if __name__ == "__main__":
    l = Lexer(source)
    p = Parser(l)
    i = Interpreter(p)
    x = i.interpret()
    print(i.GLOBAL_SCOPE)
    """
        {'number': 2, 'a': 100, 'b': 2.22, 'c': 1.12, 'name': 'mano', 'num_plus_one': 3, 'calculation': 1005, 'number_equals': False, 'number_not_equals': True, 'nested_operations': 102, 'real_div': 1.9821428571428572, 'int_div': 1.0}
    """
