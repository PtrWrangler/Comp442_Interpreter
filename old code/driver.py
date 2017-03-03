from Lexer import Lexical_Analyzer, Token
from Lexer import SCAN_ERROR, EOF
import ff_sets
import grammar_rules

"""     test input files    """
#testFile = "test_RandomSample.txt"
#testFile = "test_ID-RW_breakCases.txt"
#testFile = "test_comments.txt"
#testFile = "test_IntsAndFloats.txt"
#testFile = "test_Operators.txt"
#testFile = "test_emptyFile.txt"
#testFile = "test_allAsciiChars.txt"
#testFile = "test_MEGA_reutersFile.sgm"
testFile = "test_Utility.txt"

test_dir = "testing/"
infile = test_dir + testFile

EPSILON = ' '

'''prog_FIRST = ['class', 'program']
classDecl_FIRST = ['class', EPSILON]'''


def parse():
    with open(infile) as f:
        interpreter = Lexical_Analyzer(f.read())
        lookahead = Token(SCAN_ERROR, 0, 0, 0)

        outfile = "Outputs/Output_" + testFile
        error_log = "Outputs/ErrorLog_" + testFile

        with open(outfile, 'w+') as o:
            with open(error_log, 'w+') as err:
                while lookahead.type is not EOF:
                    lookahead = interpreter.scanner()
                    print(lookahead)

                    if lookahead.type == SCAN_ERROR:
                        err.write(lookahead.__str__() + "\n")
                    else:
                        o.write(lookahead.__str__() + "\n")


if __name__ == '__main__':
    parse()
