from Lexer import Lexical_Analyzer, Token
from Lexer import SCAN_ERROR, EOF
import ff_sets
from ff_sets import *

"""     test input files    """
# testFile = "test_MEGA_reutersFile.sgm"
#testFile = "test_Utility.txt"
testFile = "test_errRecover.txt"

test_dir = "testing/"
infile = test_dir + testFile


class Syntactic_Parser(object):
    def __init__(self):
        print "Syntactical_Parser: in __init__"

        self.outfile = "Outputs/Output_" + testFile
        self.error_log = "Outputs/ErrorLog_" + testFile
        self.f = open(infile)
        self.o = open(self.outfile, 'w+')
        self.err = open(self.error_log, 'w+')

        self.interpreter = Lexical_Analyzer(self.f.read())

        self.lookahead = Token(SCAN_ERROR, '', 0, 0)

        self.err_token = ''
        self.output = ''

    def parse(self):
        print "Syntactical_Parser: in parse"
        # self.interpreter = Lexical_Analyzer(self.f.read())

        while self.lookahead.type is not EOF:
            self.lookahead = self.interpreter.scanner()
            print(self.lookahead)

            '''if self.lookahead.type == SCAN_ERROR:
                self.err.write(self.lookahead.__str__() + "\n")
            else:
                self.output += (self.lookahead.__str__() + "\n")
            '''

            if self.prog():
                self.output += "\n\nmain parse() returning True"

            else:
                self.output += "\n\nmain parse() returning False"

            #self.prettify_output()

            self.o.write(self.output)

        self.o.close()
        self.err.close()

    def match(self, token):
        print "Syntactical_Parser: match(" + self.lookahead.value + ", " + token + ")"
        if self.lookahead.value == token:
            self.output += self.lookahead.value
            self.lookahead = self.interpreter.scanner()
            return True
        else:
            # self.lookahead = self.interpreter.scanner()
            return False

    def match_type(self, type):
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

    """ insert generated code """

