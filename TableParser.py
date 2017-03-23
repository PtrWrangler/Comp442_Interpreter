from Lexer import Lexical_Analyzer, Token
from Lexer import SCAN_ERROR, EOF, EPSILON
from Lexer import all_registered_terminals
from Grammar import Grammar, Production
from SemanticProcessor import SemanticProcessor

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
        self.errs = '\n\nERRORS OF ' + testFile + ":\n  -- ! Error locations are accurate to the original input file ! --\n\n"
        # just keeps measure of tabbing for nice output
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
        self.parsing_stack = []

        # initialize the Lexical analyser for token scanning
        self.interpreter = Lexical_Analyzer(self.f.read())
        self.lookahead = Token(EOF, EOF, '$', 0, 0)

        # Handles Semantic actions popped from parsing stack
        self.semantic_processor = SemanticProcessor()

        # print self.g
        self.initialize_parsing_table()

    def parse(self):
        print "Syntactical_Parser: in parse"

        self.parsing_stack.append(EOF)
        self.parsing_stack.append('prog')
        self.lookahead = self.interpreter.scanner()

        error = False
        while self.parsing_stack[-1] is not EOF and self.lookahead.value is not None:
            top = self.parsing_stack[-1]
            print "top       = " + top
            print "lookahead = " + self.lookahead.value

            # if top symbol is a semantic action
            if top in self.semantic_processor.dispatcher:
                print top
                # dispatches the semantic action then moves on to next symbol on stack
                self.semantic_processor.dispatcher[top]()
                self.parsing_stack.pop()

            # if top symbol is a terminal
            elif top in self.terminal_list and top != EPSILON:
                if top == self.lookahead.termtype:
                    self.format_output()

                    self.parsing_stack.pop()
                    self.semantic_processor.prevToken_buffer = self.lookahead.value
                    self.lookahead = self.interpreter.scanner()
                else:
                    print "error, wrong token"
                    self.errs += "error, wrong token. Expected: " + top + " found " + self.lookahead.__str__() + "\n"
                    error = True
                    self.handleError()
                    # self.lookahead = self.interpreter.scanner()

            # if top symbol is a grammar rule
            elif top in self.g.productions and type(self.g.productions[top]) is Production:
                # top is now the actual production of the string representation
                top = self.g.productions[top]
                #print self.lookahead

                if self.table[top.p_id][self.terminal_list.index(self.lookahead.termtype)] is not -1:
                    # top is now the corresponding correct RHS from table
                    top = self.table[top.p_id][self.terminal_list.index(self.lookahead.termtype)]

                    self.parsing_stack.pop()
                    self.parsing_stack.extend(top.inverse_RHS_multiple_push())
                    print self.parsing_stack
                else:
                    print "error, table position is -1"
                    self.errs += "table error, Expected {" + top.str_production + "} found " + self.lookahead.__str__() + '\n'
                    error = True
                    self.handleError()
                    # self.lookahead = self.interpreter.scanner()

            elif top == EPSILON:
                self.parsing_stack.pop()

            else:
                print "error, top symbol was not a SemanticSymbol / Production / token / EPSILON"
                print 'top symbol is: ' + top
                error = True
                break

            self.o.write(self.output)
            self.o.flush()
            self.output = ''

        # final parse report
        if self.lookahead.type is EOF:
            # if lookeahead i not EOF than should throw a scan error
            print "reached EOF"
        else:
            print "not EOF"

        if self.parsing_stack != ['$'] or []:
            print "Grammar did not finish, heres whats left on the stack: \n" + str(self.parsing_stack)
        else:
            print "parsing stack is empty, program parsed correctly."

        if error is True:
            print "error is True"
        else:
            print "error is False"
            self.errs += 'Source Program contains no parsing errors.\n'

            #del self.semantic_processor.SymbolTable_stack[0].entries[0].link
            self.semantic_processor.SymbolTable_stack[0].delete('Utility')
            print 'SymbolTable_stack length is: ' + \
                  str(len(self.semantic_processor.SymbolTable_stack))
            print str(self.semantic_processor.SymbolTable_stack[0])
            self.output = "\nSYMBOL TABLE STRUCTURE:\n" + (str(self.semantic_processor.SymbolTable_stack[0]))

            # check for all variable and function usage errors starting from the global table
            self.semantic_processor.SymbolTable_stack[0].IDUsageErrors([])

        self.o.write(self.errs)
        self.o.write(self.output)

        self.o.close()

        # for i in self.semantic_processor.SymbolTable_stack:
        #     print str(i) + '\n'

    # This error recovery technique syncronizes the stack and/or the lookahead to the next ;
    def handleError(self):
        print 'handling error... syncronizing to next expected sync_token'
        # print 'in error, stack: ' + str(self.parsing_stack)
        # print 'in error, lookahead: ' + str(self.lookahead.value)

        sync_tokens = [EOF, ';', '{', '}']

        # syncronizing the parsing stack to the next ;
        while self.parsing_stack[-1] not in sync_tokens:
            top = self.parsing_stack[-1]
            # print 'top: ' + top
            # print 'parsing stack: ' + str(self.parsing_stack)

            # if top is a production
            if top in self.g.productions and type(self.g.productions[top]) is Production:
                top = self.g.productions[top]

                if EPSILON not in top.str_production:
                    # expand it and push it reversed on the stack, as usual..
                    top = top.RHSs[0]
                    self.parsing_stack.pop()
                    self.parsing_stack.extend(top.inverse_RHS_multiple_push())
                    # print 'inside print parsing stack: ' + str(self.parsing_stack)
                else:
                    self.parsing_stack.pop()
            else:
                self.parsing_stack.pop()

        sync_token = self.parsing_stack[-1]

        # syncronizing the lookahead scanner to next ;
        while self.lookahead.value != sync_token:
            self.lookahead = self.interpreter.scanner()
            print 'scanning for a ' + sync_token + '... ' + self.lookahead.value

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


def print_table(table):
    for i in table:
        print i


if __name__ == '__main__':
    parser = Syntactic_Parser()
    parser.parse()

    # for i in parser.g.productions:
    #     print parser.g.productions[i].str_production
