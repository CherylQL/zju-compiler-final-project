from llvmlite import ir

TYPE = {
    "UNSIGNEDINTEGER": ir.IntType(32),
    "INTEGER": ir.IntType(32),
    "CHAR": ir.IntType(8),
    "BOOLEAN": ir.IntType(1),
    "UNSIGNEDREAL": ir.DoubleType(),
    "REAL": ir.DoubleType(),
}

IRTYPE = {
    "UNSIGNEDINTEGER": ir.IntType(32)(0).type,
    "INTEGER": ir.IntType(32)(0).type,
    "CHAR": ir.IntType(8)(0).type,
    "BOOLEAN": ir.IntType(1)(0).type,
    "UNSIGNEDREAL": ir.DoubleType()(0).type,
    "REAL": ir.DoubleType()(0).type,
}