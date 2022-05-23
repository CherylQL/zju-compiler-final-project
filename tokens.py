import ply.lex as lex
import re
# 保留字dict
reserved = {
    'and': 'AND', 'array': 'ARRAY', 'begin': 'BEGIN', 'break': 'BREAK', 'case': 'CASE', 'const': 'CONST',
    'continue': 'CONTINUE', 'default': 'DEFAULT', 'div': 'DIV', 'do': 'DO',
    'downto': 'DOWNTO', 'else': 'ELSE', 'end': 'END', 'exit': 'EXIT', 'file': 'FILE', 'for': 'FOR',
    'forward': 'FORWARD', 'function': 'FUNCTION',
    'goto': 'GOTO', 'if': 'IF', 'in': 'IN', 'label': 'LABEL', 'mod': 'MOD',
    'nil': 'NIL', 'not': 'NOT', 'of': 'OF', 'or': 'OR',
    'packed': 'PACKED', 'procedure': 'PROCEDURE', 'program': 'PROGRAM', 'read': 'READ', 'readln': 'READLN', 'record': 'RECORD',
    'repeat': 'REPEAT',  'set': 'SET', 'sizeof': 'SIZEOF', 'then': 'THEN', 'to': 'TO',
    'type': 'TYPE', 'until': 'UNTIL', 'var': 'VAR', 'while': 'WHILE', 'with': 'WITH', 'xor': 'XOR'
}


sys_func = ["abs", "chr", "odd", "ord", "pred", "sqr", "sqrt", "succ"]
sys_proc = ["write", "writeln"]
sys_con = ["false", "maxint", "true"]
sys_type = ["boolean", "char", "integer", "real", "string"]

for k in sys_func:
    reserved[k] = 'SYS_FUNCT'
for k in sys_proc:
    reserved[k] = 'SYS_PROC'
for k in sys_con:
    reserved[k] = 'SYS_CONST'
for k in sys_type:
    reserved[k] = 'SYS_TYPE'

# literal-like
sym = ('SYM_ADD', 'SYM_SUB', 'SYM_MUL', 'SYM_DIV', 'SYM_EQ', 'SYM_LT', 'SYM_GT', 'SYM_LBRAC', 'SYM_RBRAC', 'SYM_DOT',
       'SYM_COMMA', 'SYM_COLON', 'SYM_SEMICOLON', 'SYM_AT', 'SYM_CARET', 'SYM_LPAREN', 'SYM_RPAREN', 'SYM_NE', 'SYM_LE',
       'SYM_GE', 'SYM_ASSIGN', 'SYM_RANGE', 'COMMENT')

# token
tokens = list(sym) + list(set(reserved.values())) + [
        'ID', 'UNSIGNEDINTEGER', 'UNSIGNEDREAL', 'CHAR', 'STR'
    ]

t_SYM_ADD = re.escape(r'+')
t_SYM_SUB = re.escape(r'-')
t_SYM_MUL = re.escape(r'*')
t_SYM_DIV = re.escape(r'/')
t_SYM_EQ = re.escape(r'=')
t_SYM_LT = re.escape(r'<')
t_SYM_GT = re.escape(r'>')
t_SYM_LBRAC = re.escape(r'[')
t_SYM_RBRAC = re.escape(r']')
t_SYM_DOT = re.escape(r'.')
t_SYM_COMMA = re.escape(r',')
t_SYM_COLON = re.escape(r':')
t_SYM_SEMICOLON = re.escape(r';')
t_SYM_AT = re.escape(r'@')
t_SYM_CARET = re.escape(r'^')
t_SYM_LPAREN = re.escape(r'(')
t_SYM_RPAREN = re.escape(r')')
t_SYM_NE = re.escape(r'<>')
t_SYM_LE = re.escape(r'<=')
t_SYM_GE = re.escape(r'>=')
t_SYM_ASSIGN = re.escape(r':=')
t_SYM_RANGE = re.escape(r'..')


def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


# sign = r"'+|-'"
t_UNSIGNEDINTEGER = r"[0-9]+"
t_UNSIGNEDREAL = r'(\d+\.\d+(([Ee])[+-]?\d+)?)|(\d+(([Ee])[-+]?\d+))'
t_CHAR = r'\'.\''
t_STR = r'\'[^\n][^\n][^\n]*\''


t_COMMENT = r'({.*})|(\(\*(.*\n*\r*)*\*\))'
# t_ESC_CHAR = r"\'\#{INT}\'"

# Define a rule so we can track line numbers


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
