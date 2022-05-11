import tokens
import ply.lex as lex
# 使用反射机制读取上下文中的正则表达式创建lexer
lexer = lex.lex(tokens)

if __name__ == "__main__":
    f = open('Test/TestCase2.pas', 'r', encoding='utf-8')
    data = f.read()
    f.close()
    lexer.input(data)
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)

    # data = '''
    #     - 1.2e-1 - 4 * 10
    #     + 20 -2.5
    #     '''
    # # Give the lexer some input
    # lexer.input(data)
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break      # No more input
    #     print(tok.type, tok.value, tok.lineno, tok.lexpos)
