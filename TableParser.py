from Lexer import Lexical_Analyzer, Token
from Lexer import SCAN_ERROR, EOF, EPSILON
from Lexer import all_registered_terminals
from Productions import Grammar, Production, Right_hand_side
import ff_sets
from ff_sets import *
import string

"""     test input files    """
# testFile = "test_MEGA_reutersFile.sgm"
testFile = "test_Utility.txt"
#testFile = "test_errRecover.txt"
#testFile = "test_classANDprog.txt"
#testFile = "test_loopsANDifs.txt"
#testFile = "test_Arith.txt"
#testFile = "test_funcParams.txt"
#testFile = "test_expr.txt"

test_dir = "testing/"
infile = test_dir + testFile

outfile_name = testFile.split("_", 1)[1].split('.')[0] + "_Outs~Errs.txt"


class Syntactic_Parser(object):
    def __init__(self):
        print "Syntactical_Parser: in __init__"

        # Initialize logs and log messages
        self.outfile = "Outputs/" + outfile_name
        self.f = open(infile)
        self.o = open(self.outfile, 'w+')
        self.output = 'OUTPUT OF ' + testFile + ": \n\n"
        self.errs = '\n\nERRORS OF ' + testFile + ":\n\n"
        # just keeps measure of tabbng for nice output
        self.tabbed_scope = ''

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
        self.lookahead = Token(EOF, EOF, '$', 0, 0)

        # print self.g
        self.initialize_parsing_table()

    def parse(self):
        print "Syntactical_Parser: in parse"

        self.stack.append(EOF)
        self.stack.append('prog')
        self.lookahead = self.interpreter.scanner()

        error = False
        while self.stack[-1] is not EOF:
            top = self.stack[-1]
            print "top = " + top

            if top in self.terminal_list and top != EPSILON:
                if top == self.lookahead.termtype:
                    self.format_output()

                    self.stack.pop()
                    self.lookahead = self.interpreter.scanner()
                else:
                    print "error, wrong token"
                    self.errs += "error, wrong token. Expected: " + top + " found " + self.lookahead.__str__() + "\n"
                    error = True
                    self.lookahead = self.interpreter.scanner()

            elif top in self.g.productions and type(self.g.productions[top]) is Production:
                # top is now the actual production of the string representation
                top = self.g.productions[top]
                #print self.lookahead

                if self.table[top.p_id][self.terminal_list.index(self.lookahead.termtype)] is not -1:
                    # top is now the corresponding correct RHS from table
                    top = self.table[top.p_id][self.terminal_list.index(self.lookahead.termtype)]

                    self.stack.pop()
                    self.stack.extend(top.inverse_RHS_multiple_push())
                    print self.stack
                else:
                    print "error, table position is -1"
                    self.errs += "table error, Expected {" + top.str_production + "} found " + self.lookahead.__str__() + '\n'
                    error = True
                    self.lookahead = self.interpreter.scanner()

            elif top == EPSILON:
                self.stack.pop()

            else:
                print "error, top symbol was not a production/token/EPSILON"
                error = True
                break

        if self.lookahead is not EOF:
            print "not EOF"
        else:
            print "reached EOF"

        if error is True:
            print "error is True"
        else:
            print "error is False"


        #self.prettify_output()
        self.o.write(self.output)
        self.o.write(self.errs)

        self.o.close()
        #self.err.close()

    def format_output(self):
        if self.lookahead.value == ';':
            self.output += self.lookahead.value + "\n" + self.tabbed_scope

        # handle curly braces
        elif self.lookahead.value == '{':
            self.tabbed_scope += '    '
            self.output += self.lookahead.value + "\n" + self.tabbed_scope
        elif self.lookahead.value == '}':
            self.tabbed_scope = self.tabbed_scope[:-4]
            self.output += "\n" + self.tabbed_scope + self.lookahead.value

        else:
            self.output += self.lookahead.value + " "

    # create predictive parsing table
    def initialize_parsing_table(self):

        # for each production rule in the grammar
        for prod_idx in self.g.productions:
            # process each possible right-hand-side 'handle'?
            for prod_RHS in self.g.productions[prod_idx].RHSs:
                # for each terminal in the first set of this RHS
                for RHS_first in prod_RHS.first:
                    # gets its corresponding index in the terminal_list for table referencing
                    terminal_idx = self.terminal_list.index(RHS_first)

                    # store the RHS to be evaluated should you encounter this terminal with this production sitting on top of the stack.
                    self.table[self.g.productions[prod_idx].p_id][terminal_idx] = prod_RHS

                    # for prod_first in self.g.productions[prod_idx].first:
                    #     terminal_idx = self.terminal_list.index(prod_first)
                    #
                    #     # print str(prod_idx) + " " + str(prod_first)
                    #     self.table[self.g.productions[prod_idx].r_id][terminal_idx] = self.g.productions[prod_idx]

                for RHS_follow in prod_RHS.follow:
                    terminal_idx = self.terminal_list.index(RHS_follow)

                    self.table[self.g.productions[prod_idx].p_id][terminal_idx] = prod_RHS

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
