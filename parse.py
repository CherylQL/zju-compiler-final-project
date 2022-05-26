import ply.yacc as yacc
from visualize import Viz
from lex import lexer
from tokens import tokens
from CompilerError import *


class Node:
    def __init__(self, type, children, name=""):
        self.type = type
        self.children = children
        self.name = name  # 叶子节点才有自己的name

    def __repr__(self):  # 重写print用于调试
        return "(%s/%s)" % (self.type, self.name if self.name != "" else "NoName")


def p_program(p):
    'program : program_head routine SYM_DOT'
    p[0] = Node("program", [p[1], p[2], Node("SYM_DOT", [], p[3])])


def p_program_head(p):
    'program_head : PROGRAM ID SYM_SEMICOLON'
    p[0] = Node("program_head", [Node("PROGRAM", []), Node(
        "ID", [], p[2]), Node("SYM_SEMICOLON", [], p[3])])


def p_routine(p):
    'routine : routine_head routine_body'
    p[0] = Node("routine", [p[1], p[2]])


def p_sub_routine(p):
    'sub_routine : routine_head routine_body'
    p[0] = Node("subroutine", [p[1], p[2]])


def p_routine_head(p):
    'routine_head : label_part const_part type_part var_part routine_part'
    p[0] = Node("routine_head", [p[1], p[2], p[3], p[4], p[5]])


#########LABEL PART#########
def p_label_part(p):
    'label_part : epsilon'
    p[0] = Node("label_part", [p[1]])


#########CONST PART#########
def p_const_part_0(p):
    'const_part : CONST const_expr_list'
    p[0] = Node("const_part", [Node("CONST", [], p[1]), p[2]])


def p_const_part_1(p):
    'const_part : epsilon'
    p[0] = Node("const_part", [p[1]])


def p_const_expr_list_0(p):
    'const_expr_list : const_expr_list ID SYM_EQ const_value SYM_SEMICOLON'
    p[0] = Node("const_expr_list", [p[1], Node("ID", [], p[2]),
                Node("SYM_EQ", [], p[3]), p[4], Node("SYM_SEMICOLON", [], p[5])])
    # p[0].arg_list = p[1].arg_list + [[p[2], p[4].children[0].type]]


def p_const_expr_list_1(p):
    'const_expr_list : ID SYM_EQ const_value SYM_SEMICOLON'
    p[0] = Node("const_expr_list", [Node("ID", [], p[1]),
                Node("SYM_EQ", [], p[2]), p[3], Node("SYM_SEMICOLON", [], p[4])])
    # p[0].arg_list = [[p[1], p[3].children[0].type]]


def p_const_expr_list_2(p):
    'const_expr_list : const_expr_list ID SYM_EQ SYM_SUB const_value SYM_SEMICOLON'
    p[0] = Node("const_expr_list", [p[1], Node("ID", [], p[2]),
                Node("SYM_EQ", [], p[3]), Node("SYM_SUB", [], p[4]), p[5], Node("SYM_SEMICOLON", [], p[6])])
    # p[0].arg_list = p[1].arg_list + [[p[2], p[5].children[0].type]]


def p_const_expr_list_3(p):
    'const_expr_list : ID SYM_EQ SYM_SUB const_value SYM_SEMICOLON'
    p[0] = Node("const_expr_list", [Node("ID", [], p[1]),
                Node("SYM_EQ", [], p[2]), Node("SYM_SUB", [], p[3]), p[4], Node("SYM_SEMICOLON", [], p[5])])
    # p[0].arg_list = [[p[1], p[4].children[0].type]]


def p_const_value_0(p):
    'const_value : UNSIGNEDINTEGER'
    p[0] = Node("const_value", [Node("UNSIGNEDINTEGER", [], p[1])])


def p_const_value_1(p):
    'const_value : UNSIGNEDREAL'
    p[0] = Node("const_value", [Node("UNSIGNEDREAL", [], p[1])])


def p_const_value_2(p):
    'const_value : CHAR'
    p[0] = Node("const_value", [Node("CHAR", [], p[1])])


def p_const_value_3(p):
    'const_value : STR'
    p[0] = Node("const_value", [Node("STR", [], p[1])])


def p_const_value_4(p):
    'const_value : SYS_CONST'
    p[0] = Node("const_value", [Node("SYS_CONST", [], p[1])])


#########TYPE PART#########
def p_type_part_0(p):
    'type_part : TYPE type_decl_list'
    p[0] = Node("type_part", [Node("TYPE", [], p[1]), p[2]])


def p_type_part_1(p):
    'type_part : epsilon'
    p[0] = Node("type_part", [p[1]])


def p_type_decl_list_0(p):
    'type_decl_list : type_decl_list type_def'
    p[0] = Node("type_decl_list", [p[1], p[2]])


def p_type_decl_list_1(p):
    'type_decl_list : type_def'
    p[0] = Node("type_decl_list", [p[1]])


def p_type_def(p):
    'type_def : ID SYM_EQ type_decl SYM_SEMICOLON'
    p[0] = Node("type_def", [Node("ID", [], p[1]), Node(
        "SYM_EQ", [], p[2]), p[3], Node("SYM_SEMICOLON", [], p[4])])
    # t = p[3].children[0]
    # if t.type == "simple_type_decl" and t.children[0].type in ["ID", "SYS_TYPE"]:
    #     p[0].arg_list = [p[1], t.children[0].type]


def p_type_decl_0(p):
    'type_decl : simple_type_decl'
    p[0] = Node("type_decl", [p[1]])


def p_type_decl_1(p):
    'type_decl : array_type_decl'
    p[0] = Node("type_decl", [p[1]])


def p_type_decl_2(p):
    'type_decl : record_type_decl'
    p[0] = Node("type_decl", [p[1]])


def p_simple_type_decl_0(p):
    'simple_type_decl : SYS_TYPE'
    p[0] = Node("simple_type_decl", [Node("SYS_TYPE", [], p[1])])


def p_simple_type_decl_1(p):
    'simple_type_decl : ID'
    p[0] = Node("simple_type_decl", [Node("ID", [],  p[1])])


def p_simple_type_decl_2(p):
    'simple_type_decl : SYM_LPAREN name_list SYM_RPAREN'
    p[0] = Node("simple_type_decl", [
                Node("SYM_LPAREN", [], p[1]), p[2], Node("SYM_RPAREN", [], p[3])])


def p_simple_type_decl_3(p):
    'simple_type_decl : const_value SYM_RANGE const_value'
    p[0] = Node("simple_type_decl", [p[1], Node("SYM_RANGE", [], p[2]), p[3]])


def p_simple_type_decl_4(p):
    'simple_type_decl : SYM_SUB const_value SYM_RANGE const_value'
    # p[2].children[0].name = p[2].children[0].name
    p[0] = Node("simple_type_decl", [Node([], "SYM_SUB", p[1]),
                p[2], Node("SYM_RANGE", [], p[3]), p[4]])


def p_simple_type_decl_5(p):
    'simple_type_decl : SYM_SUB const_value SYM_RANGE SYM_SUB const_value'
    # p[2].children[0].name = str(- int(p[2].children[0].name))
    # p[5].children[0].name = str(- int(p[5].children[0].name))
    # p[2].children[0].name = p[2].children[0].name
    # p[5].children[0].name = p[5].children[0].name
    p[0] = Node("simple_type_decl", [Node("SYM_SUB", [], p[1]), p[2],
                Node("SYM_RANGE", [], p[3]), Node("SYM_SUB", [], p[4]), p[5]])


def p_simple_type_decl_6(p):
    'simple_type_decl : ID SYM_RANGE ID'
    p[0] = Node("simple_type_decl", [Node("ID", [],  p[1]),
                Node("SYM_RANGE", [], p[2]), Node("ID", [], p[3])])



def p_array_type_decl_0(p):
    'array_type_decl : ARRAY SYM_LBRAC simple_type_decl SYM_RBRAC OF type_decl'
    p[0] = Node("array_type_decl", [Node("ARRAY", [], p[1]), Node(
        "SYM_LBRAC", [], p[2]), p[3], Node("SYM_RBRAC", [], p[4]), Node("OF", [], p[5]), p[6]])


def p_array_type_decl_1(p):
    'array_type_decl : ARRAY SYM_LBRAC array_type_decl_part SYM_RBRAC OF type_decl'
    p[0] = Node("array_type_decl", [Node("ARRAY", [], p[1]), Node(
        "SYM_LBRAC", [], p[2]), p[3], Node("SYM_RBRAC", [], p[4]), Node("OF", [], p[5]), p[6]])

def p_array_type_decl_part(p):
    'array_type_decl_part : simple_type_decl SYM_COMMA simple_type_decl'
    p[0] = Node("array_type_decl_part", [p[1], Node("SYM_COMMA", [], p[2]),  p[3]])

def p_record_type_decl(p):
    'record_type_decl : RECORD field_decl_list END'
    p[0] = Node("record_type_decl", [
                Node("RECORD", [], p[1]), p[2], Node("END", [], p[3])])


def p_field_decl_list_0(p):
    'field_decl_list : field_decl_list field_decl'
    p[0] = Node("field_decl_list", [p[1], p[2]])


def p_field_decl_list_1(p):
    'field_decl_list : field_decl'
    p[0] = Node("field_decl_list", [p[1]])


def p_field_decl(p):
    'field_decl : name_list SYM_COLON type_decl SYM_SEMICOLON'
    p[0] = Node("field_decl", [p[1], Node("SYM_COLON", [], p[2]),
                p[3], Node("SYM_SEMICOLON", [], p[4])])


def p_name_list_0(p):
    'name_list : name_list SYM_COMMA ID'
    p[0] = Node("name_list", [p[1], Node(
        "SYM_COMMA", [], p[2]), Node("ID", [], p[3])])


def p_name_list_1(p):
    'name_list : ID'
    p[0] = Node("name_list", [Node("ID", [], p[1])])


#########VAR PART#########
def p_var_part_0(p):
    'var_part : VAR var_decl_list'
    p[0] = Node("var_part", [Node("VAR", [], p[1]), p[2]])


def p_var_part_1(p):
    'var_part : epsilon'
    p[0] = Node("var_part", [p[1]])


def p_var_decl_list_0(p):
    'var_decl_list : var_decl_list var_decl'
    p[0] = Node("var_decl_list", [p[1], p[2]])


def p_var_decl_list_1(p):
    'var_decl_list : var_decl'
    p[0] = Node("var_decl_list", [p[1]])


def p_var_decl(p):
    'var_decl : name_list SYM_COLON type_decl SYM_SEMICOLON'
    p[0] = Node("var_decl", [p[1], Node("SYM_COLON", [], p[2]),
                p[3], Node("SYM_SEMICOLON", [], p[4])])


#########FUNCTION PART#########
def p_routine_part_0(p):
    'routine_part : routine_part func_decl'
    p[0] = Node("routine_part", [p[1], p[2]])


def p_routine_part_1(p):
    'routine_part : routine_part procedure_decl'
    p[0] = Node("routine_part", [p[1], p[2]])


def p_routine_part_2(p):
    'routine_part : func_decl'
    p[0] = Node("routine_part", [p[1]])


def p_routine_part_3(p):
    'routine_part : procedure_decl'
    p[0] = Node("routine_part", [p[1]])


def p_routine_part_4(p):
    'routine_part : epsilon'
    p[0] = Node("routine_part", [p[1]])


def p_func_decl(p):
    'func_decl : func_head SYM_SEMICOLON sub_routine SYM_SEMICOLON'
    p[0] = Node("func_decl", [p[1], Node("SYM_SEMICOLON", [], p[2]),
                p[3], Node("SYM_SEMICOLON", [], p[4])])


def p_func_head(p):
    'func_head : FUNCTION ID parameters SYM_COLON simple_type_decl'
    p[0] = Node("func_head", [Node("FUNCTION", [], p[1]), Node(
        "ID", [], p[2]), p[3], Node("SYM_COLON", [], p[4]), p[5]])
    # p[0].arg_list = p[3].arg_list


def p_procedure_decl(p):
    'procedure_decl : procedure_head SYM_SEMICOLON sub_routine SYM_SEMICOLON'
    p[0] = Node("procedure_decl", [p[1], Node("SYM_SEMICOLON", [], p[2]),
                p[3], Node("SYM_SEMICOLON", [], p[4])])


def p_procedure_head(p):
    'procedure_head : PROCEDURE ID parameters'
    p[0] = Node("procedure_head", [Node("PROCEDURE", [], p[1]), Node(
        "ID", [], p[2]), p[3]])


def p_parameters(p):
    'parameters : SYM_LPAREN para_decl_list SYM_RPAREN'
    p[0] = Node("parameters", [Node("SYM_LPAREN", [], p[1]),
                p[2], Node("SYM_RPAREN", [], p[3])])
    # p[0].arg_list = p[2].arg_list


def p_parameters_e(p):
    'parameters : epsilon'
    p[0] = Node("parameters", [p[1]])


def p_para_decl_list_0(p):
    'para_decl_list : para_decl_list SYM_SEMICOLON para_type_list'
    p[0] = Node("para_decl_list", [p[1], Node(
        "SYM_SEMICOLON", [], p[2]), p[3]])
    # p[0].arg_list = p[1].arg_list + p[3].arg_list


def p_para_decl_list_1(p):
    'para_decl_list : para_type_list'
    p[0] = Node("para_decl_list", [p[1]])
    # p[0].arg_list = p[1].arg_list


def p_para_type_list_0(p):
    'para_type_list : var_para_list SYM_COLON simple_type_decl'
    p[0] = Node("para_type_list", [p[1], Node("SYM_COLON", [], p[2]), p[3]])


def p_para_type_list_1(p):
    'para_type_list : val_para_list SYM_COLON simple_type_decl'
    p[0] = Node("para_type_list", [p[1], Node("SYM_COLON", [], p[2]), p[3]])


def p_var_para_list(p):
    'var_para_list : VAR name_list'
    p[0] = Node("var_para_list", [Node("VAR", [], p[1]), p[2]])


def p_val_para_list(p):
    'val_para_list : name_list'
    p[0] = Node("val_para_list", [p[1]])


#########BODY PART#########
def p_routine_body(p):
    'routine_body : compound_stmt'
    p[0] = Node("routine_body", [p[1]])


def p_compound_stmt(p):
    'compound_stmt : BEGIN stmt_list END'
    p[0] = Node("compound_stmt", [Node("BEGIN", [], p[1]),
                p[2], Node("END", [], p[3])])


def p_stmt_list_0(p):
    'stmt_list : stmt_list stmt SYM_SEMICOLON'
    p[0] = Node("stmt_list", [p[1], p[2], Node("SYM_SEMICOLON", [], p[3])])


def p_stmt_list_1(p):
    'stmt_list : epsilon'
    p[0] = Node("stmt_list", [p[1]])


def p_stmt_0(p):
    'stmt : UNSIGNEDINTEGER SYM_COLON unlabelled_stmt'
    p[0] = Node("stmt", [Node("UNSIGNEDINTEGER", [], p[1]),
                Node("SYM_COLON", [], p[2]), p[3]])


def p_stmt_1(p):
    'stmt : unlabelled_stmt'
    p[0] = Node("stmt", [p[1]])


def p_unlabelled_stmt_0(p):
    'unlabelled_stmt : assign_stmt'
    p[0] = Node("unlabelled_stmt", [p[1]])


def p_unlabelled_stmt_1(p):
    'unlabelled_stmt : proc_stmt'
    p[0] = Node("unlabelled_stmt", [p[1]])


def p_unlabelled_stmt_2(p):
    'unlabelled_stmt : compound_stmt'
    p[0] = Node("unlabelled_stmt", [p[1]])


def p_unlabelled_stmt_3(p):
    'unlabelled_stmt : if_stmt'
    p[0] = Node("unlabelled_stmt", [p[1]])


def p_unlabelled_stmt_4(p):
    'unlabelled_stmt : repeat_stmt'
    p[0] = Node("unlabelled_stmt", [p[1]])


def p_unlabelled_stmt_5(p):
    'unlabelled_stmt : while_stmt'
    p[0] = Node("unlabelled_stmt", [p[1]])


def p_unlabelled_stmt_6(p):
    'unlabelled_stmt : for_stmt'
    p[0] = Node("unlabelled_stmt", [p[1]])


def p_unlabelled_stmt_7(p):
    'unlabelled_stmt : case_stmt'
    p[0] = Node("unlabelled_stmt", [p[1]])


def p_unlabelled_stmt_8(p):
    'unlabelled_stmt : goto_stmt'
    p[0] = Node("unlabelled_stmt", [p[1]])


def p_assign_stmt_0(p):
    'assign_stmt : ID SYM_ASSIGN expression'
    p[0] = Node("assign_stmt", [Node("ID", [], p[1]),
                Node("SYM_ASSIGN", [], p[2]), p[3]])


def p_assign_stmt_1(p):
    'assign_stmt : ID SYM_LBRAC expression SYM_RBRAC SYM_ASSIGN expression'
    p[0] = Node("assign_stmt", [Node("ID", [], p[1]), Node(
        "SYM_LBRAC", [], p[2]), p[3], Node("SYM_RBRAC", [], p[4]), Node("SYM_ASSIGN", [], p[5]), p[6]])


def p_assign_stmt_2(p):
    'assign_stmt : ID SYM_DOT ID SYM_ASSIGN expression'
    p[0] = Node("assign_stmt", [Node("ID", [], p[1]), Node(
        "SYM_DOT", [], p[2]), Node("ID", [], p[3]), Node("SYM_ASSIGN", [], p[4]), p[5]])


def p_proc_stmt_0(p):
    'proc_stmt : ID'
    p[0] = Node("proc_stmt", [Node("ID", [], p[1])])


def p_proc_stmt_1(p):
    'proc_stmt : ID SYM_LPAREN args_list SYM_RPAREN'
    p[0] = Node("proc_stmt", [Node("ID", [], p[1]), Node(
        "SYM_LPAREN", [], p[2]), p[3], Node("SYM_RPAREN", [], p[4])])


def p_proc_stmt_2(p):
    'proc_stmt : SYS_PROC'
    p[0] = Node("proc_stmt", [Node("SYS_PROC", [], p[1])])


def p_proc_stmt_3(p):
    'proc_stmt : SYS_PROC SYM_LPAREN expression_list SYM_RPAREN'
    p[0] = Node("proc_stmt", [Node("SYS_PROC", [], p[1]),
                Node("SYM_LPAREN", [], p[2]), p[3], Node("SYM_RPAREN", [], p[4])])


def p_proc_stmt_4(p):
    'proc_stmt : READ SYM_LPAREN factor SYM_RPAREN'
    p[0] = Node("proc_stmt", [Node("READ", []), Node(
        "SYM_LPAREN", [], p[2]), p[3], Node("SYM_RPAREN", [], p[4])])


def p_if_stmt(p):
    'if_stmt : IF expression THEN stmt else_clause'
    p[0] = Node("if_stmt", [Node("IF", [], p[1]), p[2],
                Node("THEN", [], p[3]), p[4], p[5]])


def p_else_clause_0(p):
    'else_clause : ELSE stmt'
    p[0] = Node("else_clause", [Node("ELSE", [], p[1]), p[2]])


def p_else_clause_1(p):
    'else_clause : epsilon'
    p[0] = Node("else_clause", [p[1]])


def p_repeat_stmt(p):
    'repeat_stmt : REPEAT stmt_list UNTIL expression'
    p[0] = Node("repeat_stmt", [Node("REPEAT", [], p[1]),
                p[2], Node("UNTIL", [], p[3]), p[4]])


def p_while_stmt(p):
    'while_stmt : WHILE expression DO stmt'
    p[0] = Node("while_stmt", [Node("WHILE", [], p[1]),
                p[2], Node("DO", [], p[3]), p[4]])


def p_for_stmt(p):
    'for_stmt : FOR ID SYM_ASSIGN expression direction expression DO stmt'
    p[0] = Node("for_stmt", [Node("FOR", [], p[1]), Node("ID", [], p[2]), Node(
        "SYM_ASSIGN", [], p[3]), p[4], p[5], p[6], Node("DO", [], p[7]), p[8]])


def p_direction_0(p):
    'direction : TO'
    p[0] = Node("direction", [Node("TO", [], p[1])])


def p_direction_1(p):
    'direction : DOWNTO'
    p[0] = Node("direction", [Node("DOWNTO", [], p[1])])


def p_case_stmt(p):
    'case_stmt : CASE expression OF case_expr_list END'
    p[0] = Node("case_stmt", [Node("CASE", [], p[1]), p[2],
                Node("OF", [], p[3]), p[4], Node("END", [], p[5])])


def p_case_expr_list_0(p):
    'case_expr_list : case_expr_list case_expr'
    p[0] = Node("case_expr_list", [p[1], p[2]])


def p_case_expr_list_1(p):
    'case_expr_list : case_expr'
    p[0] = Node("case_expr_list", [p[1]])


def p_case_expr_1(p):
    'case_expr : const_value SYM_COLON stmt SYM_SEMICOLON'
    p[0] = Node("case_expr", [p[1], Node("SYM_COLON", [], p[2]),
                p[3], Node("SYM_SEMICOLON", [], p[4])])


def p_case_expr_2(p):
    'case_expr : ID SYM_COLON stmt SYM_SEMICOLON'
    p[0] = Node("case_expr", [Node("ID", [], p[1]), Node(
        "SYM_COLON", [], p[2]), p[3], Node("SYM_SEMICOLON", [], p[4])])


def p_goto_stmt(p):
    'goto_stmt : GOTO UNSIGNEDINTEGER'
    p[0] = Node("goto_stmt", [Node("GOTO", [], p[1]),
                Node("UNSIGNEDINTEGER", [], p[2])])


def p_expression_list_0(p):
    'expression_list : expression_list SYM_COMMA expression'
    p[0] = Node("expression_list", [p[1], Node("SYM_COMMA", [], p[2]), p[3]])


def p_expression_list_1(p):
    'expression_list : expression'
    p[0] = Node("expression_list", [p[1]])


def p_expression_0(p):
    '''expression : expression SYM_GE expr'''
    p[0] = Node("expression", [p[1], Node("SYM_GE", [], p[2]), p[3]])


def p_expression_1(p):
    '''expression : expression SYM_GT expr'''
    p[0] = Node("expression", [p[1], Node("SYM_GT", [], p[2]), p[3]])


def p_expression_2(p):
    '''expression : expression SYM_LE expr'''
    p[0] = Node("expression", [p[1], Node("SYM_LE", [], p[2]), p[3]])


def p_expression_3(p):
    '''expression : expression SYM_LT expr'''
    p[0] = Node("expression", [p[1], Node("SYM_LT", [], p[2]), p[3]])


def p_expression_4(p):
    '''expression : expression SYM_EQ expr'''
    p[0] = Node("expression", [p[1], Node("SYM_EQ", [], p[2]), p[3]])


def p_expression_5(p):
    '''expression : expression SYM_NE expr'''
    p[0] = Node("expression", [p[1], Node("SYM_NE", [], p[2]), p[3]])


def p_expression_6(p):
    'expression : expr'
    p[0] = Node("expression", [p[1]])
    

def p_expression_7(p):
    'expression : expression SYM_COMMA expr'
    p[0] = Node("expression",[p[1], Node("SYM_COMMA", [], p[2]), p[3]])


def p_expr_0(p):
    'expr : expr SYM_ADD term'
    p[0] = Node("expr", [p[1], Node("SYM_ADD", [], p[2]), p[3]])


def p_expr_1(p):
    'expr : expr SYM_SUB term'
    p[0] = Node("expr", [p[1], Node("SYM_SUB", [], p[2]), p[3]])


def p_expr_2(p):
    'expr : expr OR term'
    p[0] = Node("expr", [p[1], Node("OR", [], p[2]), p[3]])


def p_expr_3(p):
    'expr : term'
    p[0] = Node("expr", [p[1]])


def p_term_0(p):
    'term : term SYM_MUL factor'
    p[0] = Node("term", [p[1], Node("SYM_MUL", [], p[2]), p[3]])


def p_term_1(p):
    'term : term SYM_DIV factor'
    p[0] = Node("term", [p[1], Node("SYM_DIV", [], p[2]), p[3]])


def p_term_2(p):
    'term : term MOD factor'
    p[0] = Node("term", [p[1], Node("MOD", [], p[2]), p[3]])


def p_term_3(p):
    'term : term AND factor'
    p[0] = Node("term", [p[1], Node("AND", [], p[2]), p[3]])


def p_term_4(p):
    'term : factor'
    p[0] = Node("term", [p[1]])


def p_factor_0(p):
    'factor : ID'
    p[0] = Node("factor", [Node("ID", [], p[1])])


def p_factor_1(p):
    'factor : ID SYM_LPAREN args_list SYM_RPAREN'
    p[0] = Node("factor", [Node("ID", [], p[1]), Node(
        "SYM_LPAREN", [], p[2]), p[3], Node("SYM_RPAREN", [], p[4])])


def p_factor_2(p):
    'factor : SYS_FUNCT'
    p[0] = Node("factor", [Node("SYS_FUNCT", [], p[1])])


def p_factor_3(p):
    'factor : SYS_FUNCT SYM_LPAREN args_list SYM_RPAREN'
    p[0] = Node("factor", [Node("SYS_FUNCT", [], p[1]), Node(
        "SYM_LPAREN", [], p[2]), p[3], Node("SYM_RPAREN", [], p[4])])


def p_factor_4(p):
    'factor : const_value'
    p[0] = Node("factor", [p[1]])


def p_factor_5(p):
    'factor : SYM_LPAREN expression SYM_RPAREN'
    p[0] = Node("factor", [Node("SYM_LPAREN", [], p[1]),
                p[2], Node("SYM_RPAREN", [], p[3])])


def p_factor_6(p):
    'factor : NOT factor'
    p[0] = Node("factor", [Node("NOT", [], p[1]), p[2]])


def p_factor_7(p):
    'factor : SYM_SUB factor'
    p[0] = Node("factor", [Node("SYM_SUB", [], p[1]), p[2]])


def p_factor_8(p):
    'factor : ID SYM_LBRAC expression SYM_RBRAC'
    p[0] = Node("factor", [Node("ID", [], p[1]), Node(
        "SYM_LBRAC", [], p[2]), p[3], Node("SYM_RBRAC", [], p[4])])


def p_factor_9(p):
    'factor : ID SYM_DOT ID '
    p[0] = Node("factor", [Node("ID", [], p[1]), Node(
        "SYM_DOT", [], p[2]), Node("ID", [], p[3])])


def p_args_list_0(p):
    'args_list : args_list SYM_COMMA expression'
    p[0] = Node("args_list", [p[1], Node("SYM_COMMA", [], p[2]), p[3]])


def p_args_list_1(p):
    'args_list : expression'
    p[0] = Node("args_list", [p[1]])


def p_epsilon(p):
    'epsilon : '
    p[0] = Node("epsilon", [])


def p_error(p):
    print("Syntax error in input!", p)
    raise ParsingException(["Syntax error: %s at %d" % (p.value, p.lineno)])


parser = yacc.yacc()

if __name__ == "__main__":
    f = open('./Test/Qsort.pas', 'r', encoding='utf-8')
    data = f.read()
    f.close()
    result = parser.parse(data)
    # print(result)
    Viz(result).png()

