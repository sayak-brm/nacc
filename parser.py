#! /usr/bin/python3

from lexer import Lexer, Tokens, compile_exprs

class ParserError(Exception): pass

class Node:
    def __init__(self, _tag, _params, _children):
        self.tag = _tag
        self.params = _params
        self.children = _children

    def get_code(self, gen_lib):
        return gen_lib[self.tag]

    def __repr__(self):
        if not self.children: return self.tag
        return self.tag + '\n' + '\n'.join(
            [child.__repr__() for child in self.children])

class Parser:
    def __init__(self, toks):
        self.toks=toks
        self.cur=0

    def parse(self):
        return self.Program()

    def Int(self):
        if self.toks[self.cur].tag == "INT_LITERAL":
            return Node("INT",
                [self.toks[self.cur].text], None)

    def Expression(self):
        expr = None
        if self.toks[self.cur].tag == "INT_LITERAL":
            expr = self.Int()
        if not expr:
            raise ParserError(
                "Expected expression:\n" +
                self.toks[self.cur].text)
        self.cur+=1

        return Node("EXPR", None, [expr])

    def Statement(self):
        if self.toks[self.cur].tag != "RETURN":
            raise ParserError(
                "Expected return Keyword:\n" +
                self.toks[self.cur].text)
        self.cur+=1

        ret = Node("STMT", None, [self.Expression()])

        if self.toks[self.cur].tag != "SEMICOLON":
            raise ParserError(
                "Expected semicolon:\n" +
                self.toks[self.cur].text)
        self.cur+=1

        return ret

    def Function(self):
        fn_type = None
        if self.toks[self.cur].tag == "INT":
            fn_type = self.toks[self.cur].tag
        if not fn_type:
            raise ParserError(
                "Invalid return type for function:\n" +
                self.toks[self.cur].text)
        self.cur+=1

        name = None
        if self.toks[self.cur].tag == "IDENTIFIER":
            name = self.toks[self.cur].text
        if not name:
            raise ParserError(
                "Invalid name for function:\n" +
                self.toks[self.cur].text)
        self.cur+=1

        if self.toks[self.cur].tag != "OPEN_PAREN" and \
            self.toks[self.cur+1].tag != "CLOSED_PAREN":
            raise ParserError(
                "Invalid function declaration:\n" +
                self.toks[self.cur].text)
        self.cur+=2

        if self.toks[self.cur].tag != "OPEN_BRACE":
            raise ParserError(
                "Expected Opening Brace:\n" +
                self.toks[self.cur].text)
        self.cur+=1

        ret = Node("FUNC", [name, fn_type],
            [self.Statement()])

        if self.toks[self.cur].tag != "CLOSED_BRACE":
            raise ParserError(
                "Expected Closing Brace:\n" +
                self.toks[self.cur].text)
        self.cur+=1

        return ret

    def Program(self):
        return Node("PROG", None, [self.Function()])

if __name__ == "__main__":
    """Tests the parser using sample code.
    """
    code='''
int main() {
    return 2;
}
'''
    print('{}\nTokens:'.format(code))
    toks = Lexer(code).lex(compile_exprs(Tokens.types))
    for tok in toks:
        print(tok)
    parser = Parser(toks)
    print('\nAST:\n{}'.format(parser.parse()))