#! /usr/bin/python3

import re
import string

from partpy import SourceString, PartpyError

class Token:
    """The Token class represents indivudual lexed tokens.
    """
    def __init__(self, tag, text):
        """Initializes each token.

        Arguments:
            tag {str} -- Token Type
            text {str} -- Token Text
        """
        self.tag=tag
        self.text=text

    def __repr__(self):
        """Pretty-printing for tokens.
        """
        return "{} {}token with text:  {}".format(
            self.tag, '\t'*(2-len(self.tag)//7), self.text)

class Tokens(list):
    """List subclass for storing lexed tokens.
    """
    types = [
        ('OPEN_BRACE',      r'{'),
        ('CLOSED_BRACE',    r'}'),
        ('OPEN_PAREN',      r'\('),
        ('CLOSED_PAREN',    r'\)'),
        ('SEMICOLON',       r';'),
        ('INT',             r'int'),
        ('RETURN',          r'return'),
        ('IDENTIFIER',      r'[a-zA-Z]\w*'),
        ('INT_LITERAL',     r'[0-9]+')
    ]

class Lexer(SourceString):
    """Lexer for splitting and classifying tokens.

    Raises:
        PartpyError: Unknown/Illegal character in input.
    """
    def lex(self, exprs):
        """Lexer function

        Arguments:
            exprs {tuple} -- (Expr Tag, Token Regex)

        Raises:
            PartpyError: Unknown/Illegal character in input.

        Returns:
            Tokens(list) -- List of lexed tokens.
        """
        toks=Tokens()
        while not self.eos:
            self.skip_whitespace(1)
            match = None
            for expr in exprs:
                tag, regex = expr
                match = regex.match(self.rest_of_string())
                if match:
                    text = match.group(0)
                    toks.append(Token(tag, text))
                    break
            if not match:
                raise PartpyError(self,
                    msg="Illegal Character")
            else: self.eat_length(match.end(0))
            self.skip_whitespace(1)
        return toks

def compile_exprs(exprs):
    """Compiles regex expressions.

    Arguments:
        exprs {tuple} -- (Expr Tag, Regex String)

    Returns:
        tuple -- (Expr Tag, Compiled Regex)
    """
    i=0
    for expr in exprs:
        exprs[i] = (expr[0], re.compile(expr[1]))
        i+=1
    return exprs

if __name__ == '__main__':
    """Tests the lexer using sample code.
    """
    code='''
int main() {
    return 2;
}
'''
    print('{}\nTokens:'.format(Lexer(code).lex(
        compile_exprs(Tokens.types))))
    for tok in lex(code):
        print(tok)