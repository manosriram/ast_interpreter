class Symbol(object):
    def __init__(self, name, var_type=None) -> None:
        self.name = name
        self.type = var_type

class BuiltInTypeSymbol(Symbol):
    def __init__(self, name) -> None:
        super().__init__(name)

    def __str__(self) -> str:
        return self.name
    
    __repr__ = __str__

class VarSymbol(Symbol):
    def __init__(self, name, var_type=None) -> None:
        super().__init__(name, var_type)

    def __str__(self) -> str:
        return f"{self.name} : {self.type}"

    __repr__ = __str__

class SymbolTable(object):

    def __init__(self) -> None:
        self.symbols = {}
        self.init_builtin_types()

    def init_builtin_types(self):
        self.define(BuiltInTypeSymbol("INTEGER"))
        self.define(BuiltInTypeSymbol("REAL"))

    def __str__(self):
        s = 'Symbols: {symbols}'.format(
            symbols=[value for value in self.symbols.values()]
        )
        return s 

    def define(self, symbol):
        self.symbols[symbol.name] = symbol

    def lookup(self, name):
        return self.symbols.get(name, None)

    __repr__ = __str__
