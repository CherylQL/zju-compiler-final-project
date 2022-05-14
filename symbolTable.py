from CompilerError import *

class SymbolTable:
    def __init__(self):
        self.SymTables = []

    def initial(self):
        self.SymTables.append({})

    def find(self, target):
        stbLength = len(self.SymTables)
        for i in range(stbLength - 1, -1, -1):
            if target in self.SymTables[i]:
                return self.SymTables[i][target]
        raise DefMissingException(("DefMissingException: undefined symbol: %s" % target))
        return  None

    def insert(self, stb, idx = -1):
        if stb[0] in self.SymTables[-1].keys():
            raise MulDefException(("MulDefException: Duplicate symbol: %s" % stb[0]))
        self.SymTables[idx][stb[0]] = {"entry" : stb[1]}