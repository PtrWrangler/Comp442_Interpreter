from Lexer import Lexical_Analyzer, Token
from Lexer import SCAN_ERROR, EOF
from Lexer import all_registered_terminals
from Productions import Grammar, Production
import ff_sets
from ff_sets import *
import string

"""     test input files    """
# testFile = "test_MEGA_reutersFile.sgm"
#testFile = "test_Utility.txt"
#testFile = "test_errRecover.txt"
#testFile = "test_classANDprog.txt"
#testFile = "test_loopsANDifs.txt"
#testFile = "test_Arith.txt"
#testFile = "test_funcParams.txt"
testFile = "test_expr.txt"

test_dir = "testing/"
infile = test_dir + testFile


class Syntactic_Parser(object):
    def __init__(self):
        print "Syntactical_Parser: in __init__"

        # Initialize logs and log messages
        self.outfile = "Outputs/Output_" + testFile
        self.error_log = "Outputs/ErrorLog_" + testFile
        self.f = open(infile)
        self.o = open(self.outfile, 'w+')
        self.err = open(self.error_log, 'w+')
        self.err_token = ''
        self.output = ''

        # generate grammar object from the specs file
        self.g = Grammar()

        # culminate list of all possible terminals
        self.terminal_list = []
        for terminal_set in all_registered_terminals:
            for terminal in terminal_set:
                self.terminal_list.append(terminal)

        # initialize all table to -1
        self.table = [[-1 for x in range(len(self.terminal_list))] for y in range(len(self.g.productions))]
        # stack to be used for the table predictive parsing method
        self.stack = []

        # initialize the Lexical analyser for token scanning
        self.interpreter = Lexical_Analyzer(self.f.read())
        self.lookahead = Token(EOF, '$', 0, 0)

        self.initialize_parsing_table()

    def parse(self):
        print "Syntactical_Parser: in parse"

        self.stack.append(Token(EOF, '$', 0, 0))
        self.stack.append(self.g.productions[0])
        self.lookahead = self.interpreter.scanner()

        error = False
        while self.stack[-1] is not EOF:
            top = self.stack[-1]

            if type(top) is Token and top.termtype in self.terminal_list:
                if top.value == self.lookahead.value:
                    self.stack.pop()
                    self.lookahead = self.interpreter.scanner()
                else:
                    print "error"
                    error = True
                    break

            elif type(top) is Production:
                if self.table[top.r_id][self.terminal_list.index(self.lookahead.termtype)] is not -1:
                    self.stack.pop()

            else:
                print "error, top symbol was not a production or token"
                error = True


        #self.prettify_output()
        #self.o.write(self.output)

        self.o.close()
        self.err.close()

    def initialize_parsing_table(self):

        # create predictive parsing table
        for prod_idx in self.g.productions:
            for prod_first in self.g.productions[prod_idx].first:
                terminal_idx = self.terminal_list.index(prod_first)

                # print str(prod_idx) + " " + str(prod_first)
                self.table[prod_idx][terminal_idx] = self.g.productions[prod_idx]

            for prod_follow in self.g.productions[prod_idx].follow:
                terminal_idx = self.terminal_list.index(prod_follow)
                table[prod_idx][terminal_idx] = self.g.productions[prod_idx]

        print_table(self.table)

    def match(self, token):
        if self.lookahead.value is not None:
            print "Syntactical_Parser: match(" + self.lookahead.value + ", " + token + ")"
        if self.lookahead.value == token:
            self.output += self.lookahead.value
            self.lookahead = self.interpreter.scanner()
            return True
        else:
            # self.lookahead = self.interpreter.scanner()
            return False

    def match_type(self, type):
        if self.lookahead.value is not None:
            print "Syntactical_Parser: match_type(" + self.lookahead.type + ", " + type + ")"
        if self.lookahead.type == type:
            self.output += self.lookahead.value
            self.lookahead = self.interpreter.scanner()
            return True
        else:
            # self.lookahead = self.interpreter.scanner()
            return False

    def is_type_Id(self):
        if self.lookahead.type == 'Id':
            return True
        else:
            return False

    def prettify_output(self):
        # self.o = open(self.outfile, 'rw+')
        scope = 0
        tabs = ''
        newline = False
        for c in self.output:
            if c == '}':
                tabs = tabs[:-4]

            elif c == '{':
                tabs += '    '
                c = '{\n'

            elif c == ';':
                c = ';\n'

            self.o.write(c)


def print_table(table):
    for i in table:
        print i


if __name__ == '__main__':
    parser = Syntactic_Parser()
    parser.parse()
