#! /usr/bin/python3

import re
import string

from partpy import SourceString, PartpyError

class Tokens(list):
    types = [
        ('OPEN_BRACE', '{'),
        ('CLOSED_BRACE', '}'),
        ('OPEN_PAREN', '\\('),
        ('CLOSED_PAREN', '\\)'),
        ('SEMICOLON', ';'),
        ('INT', 'int'),
        ('RETURN', 'return'),
        ('IDENTIFIER', '[a-zA-Z]\\w*'),
        ('INT_LITERAL', '[0-9]+')
    ]

class Lexer(SourceString):
    def lex(self, exprs):
        toks=Tokens()
        while not self.eos:
            self.skip_whitespace(1)
            match = None
            for expr in exprs:
                tag, regex = expr
                match = regex.match(self.rest_of_string())
                if match:
                    text = match.group(0)
                    toks.append((tag, text))
                    break
            if not match:
                raise PartpyError(self, msg="Illegal Character")
            else: self.eat_length(match.end(0))
        return toks

def compile_exprs(exprs):
    i=0
    for expr in exprs:
        exprs[i] = (expr[0], re.compile(expr[1]))
        i+=1
    return exprs

def lex(s):
    return Lexer(s).lex(compile_exprs(Tokens.types))

if __name__ == '__main__':
    code='''int main() {
        return 2;
    }'''
    print('CODE:\n\n', code, '\n\nTokens:')
    for tok in lex(code):
        print(tok)