import string
import re

reserved_words = ['and', 'not', 'or', 'if', 'then', 'else', 'for',
                  'class', 'int', 'float', 'get', 'put', 'return', 'program']
compare_operators = ['==', '<>', '<', '>', '<=', '>=']
math_operators = ['+', '-', '*', '/']
assign_operators = ['=']
punctuations = [';', ',', '.', '(', ')', '{', '}', '[', ']']
comments = ['//', '/*', '*/']

# Token types
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
IDENTIFIER, KEYWORD = 'ID', 'KEYWORD'
INTEGER, FLOAT = 'INT', 'FLOAT'
COMPARE_OP, MATH_OP, ASSIGN_OP = 'COMPARE_OP', 'MATH_OP', 'ASSIGN_OP'
#PUNCTUATION = 'PUNCTUATION'

SEMI_COLON, COMMA, PERIOD = 'SEMI_COLON', 'COMMA', 'PERIOD'
BRACKET_OPEN, BRACKET_CLOSE, CURLY_OPEN, CURLY_CLOSE, SQUARE_OPEN, SQUARE_CLOSE = \
    'BRACKET_OPEN', 'BRACKET_CLOSE', 'CURLY_OPEN', 'CURLY_CLOSE', 'SQUARE_OPEN', 'SQUARE_CLOSE'
INLINE_COMMENT, BLOCK_COMMENT_OPEN, BLOCK_COMMENT_CLOSE = 'INLINE_COMMENT', 'BLOCK_COMMENT_OPEN', 'BLOCK_COMMENT_CLOSE'

COMMENT = 'COMMENT'
EOF = '$'
SCAN_ERROR = 'SCAN_ERROR'
EPSILON = 'EPSILON'

all_registered_terminals = [reserved_words, compare_operators, math_operators, assign_operators, punctuations, comments, [IDENTIFIER, INTEGER, FLOAT, EPSILON, EOF]]


class Token(object):
    def __init__(self, type, termtype, value, line, pos):
        # token type: INTEGER, PLUS, MINUS, or EOF
        self.type = type
        # need one variable to do comparsons in parsing, type and value cant both be used. mainly for ID.
        self.termtype = termtype
        # token value: non-negative integer value, '+', '-', or None
        self.value = value
        # location(position) in the source code
        self.line = line
        self.pos = pos

    def __str__(self):
        """String representation of the class instance."""

        # return self.value
        return 'Token({termtype}, {value}, Line:Pos=({line}, {pos}))'.format(
            # type=self.type,
            termtype=self.termtype,
            value=repr(self.value),
            line=self.line,
            pos=self.pos
        )

    def __repr__(self):
        return self.__str__()


class Lexical_Analyzer(object):
    def __init__(self, text):
        # client string input, only accept basic printable ascii characters (basic english keyboard stuff)
        self.text = filter(lambda x: x in string.printable, text)
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

        # handle initializing potential empty input file
        if self.text == '':
            self.text = ' '
        self.current_char = self.text[self.pos]

        # keeps track of line number and cursor position for proper token/error reporting
        self.line_number = 1
        self.line_pos = 1

    '''def error(self):
        raise Exception('Error parsing input')'''

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        if self.current_char == '\n':
            self.line_number += 1
            self.line_pos = 1
        else:
            self.line_pos += 1

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def jump_cursor(self, cursor_spaces):
        while cursor_spaces > 0:
            # advance the length of the match before returning
            self.advance()
            cursor_spaces -= 1

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def keyword_or_identifier(self):
        # starter is a letter, Could become reserved word or identifier
        token = ''

        # at this point it could be an id or a reserved word
        # keep eating all letters, digits and _
        while self.current_char is not None and \
                self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_':
            # print "alpha:", self.current_char
            token += self.current_char
            self.advance()

        # token = token.lower()
        if token in reserved_words:
            print "reserved word: ", token
            return Token(KEYWORD, token, token, self.line_number, self.line_pos)
        else:
            print "identifier: ", token
            return Token(IDENTIFIER, IDENTIFIER, token, self.line_number, self.line_pos)

    def integer_or_float(self):
        """Return a integer or float consumed from the input."""
        '''If a '.' is not preceded or followed by at least one digit,
            it is just a period (punctuation)'''

        text = self.text[self.pos:]
        result = ''

        """will match any float with at least 1 digit before OR after the decimal
            rejects leading and trailing 0s, with exception of them touching the decimal"""
        match = re.search("^([1-9]\d*|0)\.(\d*[1-9]|0)|^\.(\d*[1-9]|0)", text)
        if match:
            result = match.group()
            self.jump_cursor(match.span()[1])
            return Token(FLOAT, FLOAT, result, self.line_number, self.line_pos)

        """Will match any integer string that doesnt start in 0, or matches a simple 0 int"""
        match = re.search("^[1-9]+\d*|^0", text)
        if match:
            result = match.group()
            self.jump_cursor(match.span()[1])
            return Token(INTEGER, INTEGER, result, self.line_number, self.line_pos)

        result = '.'
        self.advance()
        return Token(PERIOD, result, result, self.line_number, self.line_pos)

        """Matches a period (not decimal / failed float test)"""
        '''match = re.search('^\.', text)
        if match:
            result = '.'
            self.advance()
            return Token(PERIOD, result, self.line_number, self.line_pos)

        # should never reach this point
        print "SCAN_ERROR: there was no int/float/period matches"
        return Token(SCAN_ERROR, "int/float/period problem: " + result, self.line_number, self.line_pos)'''

    def operator_or_punctuation(self):
        """
        tokens that can immediately return:
            + - ( ) [ ] { } . , ;

        tokens that require checking next char:
            =  (=, ==)
            <  (<, <>, <=)
            >  (>, >=)
            *  (*, */)
            /  (/, //, /*)
        """
        """ASSUMING ALL OPS AND PUNCTS ARE MAX ONLY 2 CHARS, THIS METHOD WORKS QUICKEST"""

        token = self.current_char
        self.advance()

        if self.current_char is not None:
            token = token + self.current_char
            # print "2char op or punct?:", token

            if token in compare_operators:
                self.advance()
                return Token(COMPARE_OP, token, token, self.line_number, self.line_pos)
            if token in math_operators:
                self.advance()
                return Token(MATH_OP, token, token, self.line_number, self.line_pos)
            if token in assign_operators:
                self.advance()
                return Token(ASSIGN_OP, token, token, self.line_number, self.line_pos)
            if token in comments:
                self.advance()
                return Token(COMMENT, token, token, self.line_number, self.line_pos)

        # if all double puncts or ops have failed try only single char ones
        # print "1char op or punct?:", token[0]
        if token[0] in compare_operators:
            return Token(COMPARE_OP, token[0], token[0], self.line_number, self.line_pos)
        if token[0] in math_operators:
            return Token(MATH_OP, token[0], token[0], self.line_number, self.line_pos)
        if token[0] in assign_operators:
            return Token(ASSIGN_OP, token[0], token[0], self.line_number, self.line_pos)

        '''if token[0] in punctuations:
            return Token(PUNCTUATION, token[0], self.line_number, self.line_pos)'''
        if token[0] == ';':
            return Token(SEMI_COLON, token[0], token[0], self.line_number, self.line_pos)
        if token[0] == ',':
            return Token(COMMA, token[0], token[0], self.line_number, self.line_pos)
        if token[0] == '(':
            return Token(BRACKET_OPEN, token[0], token[0], self.line_number, self.line_pos)
        if token[0] == ')':
            return Token(BRACKET_CLOSE, token[0], token[0], self.line_number, self.line_pos)
        if token[0] == '{':
            return Token(CURLY_OPEN, token[0], token[0], self.line_number, self.line_pos)
        if token[0] == '}':
            return Token(CURLY_CLOSE, token[0], token[0], self.line_number, self.line_pos)
        if token[0] == '[':
            return Token(SQUARE_OPEN, token[0], token[0], self.line_number, self.line_pos)
        if token[0] == ']':
            return Token(SQUARE_CLOSE, token[0], token[0], self.line_number, self.line_pos)

        # all registered punctuations and operators have been tried, unrecognized character
        print "SCAN_ERROR: Unregistered punctuation: " + token[0]
        return Token(SCAN_ERROR, SCAN_ERROR, "Unregistered punctuation: " + token[0], self.line_number, self.line_pos)

    def scanner(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            elif self.current_char.isalpha():
                return self.keyword_or_identifier()

            elif self.current_char.isdigit() or self.current_char == '.':
                return self.integer_or_float()

            # catch all punctuation, except period which is part of floats/ints
            elif self.current_char in string.punctuation:
                return self.operator_or_punctuation()

            else:
                char = self.current_char
                self.advance()
                print "SCAN_ERROR: Unregistered Character: " + str(char)
                return Token(SCAN_ERROR, SCAN_ERROR, "Unregistered Character: " + str(char), self.line_number, self.line_pos)

        return Token(EOF, EOF, None, self.line_number, self.line_pos)

