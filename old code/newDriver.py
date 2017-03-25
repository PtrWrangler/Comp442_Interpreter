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
        self.EPSILON = 'EPSILON'

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

    def prog(self):  # LHS-RHS1 | RHS2 |
        print "Syntactical_Parser: in prog"
        if self.lookahead.value in ff_sets.prog_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.classDecl() and self.progBody():
                    print "prog -> classDecl progBody"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: prog(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def classDecl(self):
        print "Syntactical_Parser: in classDecl"
        if self.lookahead.value in ff_sets.classDecl_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('class') and self.match_type('Id') and self.match('{') and self.classBody() and self.match(
                        '}') and self.match(';') and self.classDecl():

                    print "classDecl -> class Id { classBody } ; classDecl "

                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: classDecl(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.classDecl_FOLLOW:
            print "classDecl -> EPSILON"
            return True
        else:
            return False

    def classBody(self):
        print "Syntactical_Parser: in classBody"
        if self.lookahead.value in ff_sets.classBody_FIRST1 or self.is_type_Id():  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.type() and self.match_type('Id') and self.varOrFunc():

                    print "classBody -> type Id varOrFunc"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: classBody(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.classBody_FOLLOW:
            print "classBody -> EPSILON"
            return True
        else:
            return False

    def varOrFunc(self):
        print "Syntactical_Parser: in varOrFunc"
        if self.lookahead.value in ff_sets.varOrFunc_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.indice() and self.match(';') and self.classBody():

                    print "varOrFunc -> indice ; classBody"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: varOrFunc(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.varOrFunc_FIRST2:
            while self.lookahead.type != '$':
                if self.match('(') and self.fParams() and self.match(')') and self.funcBody() and self.match(';') and self.classBody():

                    print "varOrFunc -> ( fParams ) funcBody classBody"

                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: varOrFunc(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def progBody(self):
        print "Syntactical_Parser: in progBody"
        if self.lookahead.value in ff_sets.progBody_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('program') and self.funcBody() and self.match(';') and self.funcDef():
                    print "progBody -> program funcBody ; funcDef"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: progBody(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def funcHead(self):
        print "Syntactical_Parser: in funcHead"
        if self.lookahead.value in ff_sets.funcHead_FIRST1 or self.is_type_Id():  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.type() and self.match_type('Id') and self.match('(') and self.fParams() and self.match(')'):
                    print "funcHead -> type Id ( fParams )"

                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: funcHead(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def funcDef(self):
        print "Syntactical_Parser: in funcDef"
        if self.lookahead.value in ff_sets.funcDef_FIRST1 or self.is_type_Id():  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.funcHead() and self.funcBody() and self.match(';') and self.funcDef():

                    print "funcDef -> funcHead funcBody ; funcDef"

                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: funcDef(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.type in ff_sets.funcDef_FOLLOW:
            print "funcDef -> EPSILON"
            return True
        else:
            return False

    def funcBody(self):
        print "Syntactical_Parser: in funcBody"
        if self.lookahead.value in ff_sets.funcBody_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('{') and self.gen_statements() and self.match('}'):
                    print "funcBody -> { gen_statements }"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: funcBody(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def varDecl(self):
        print "Syntactical_Parser: in varDecl"
        if self.lookahead.type in ff_sets.varDecl_FIRST1 or self.is_type_Id():  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.UD_Type() and self.createOrAssign() and self.varDeclTail():

                    print "varDecl -> UD_Type createOrAssign varDeclTail"
                    # self.output += '\n'
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: varDecl(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.varDecl_FIRST2:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.P_Type() and self.match_type('Id') and self.varDeclTail():

                    print "varDecl -> P_Type Id varDeclTail"
                    # self.output += '\n'
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: varDecl(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def createOrAssign(self):
        print "Syntactical_Parser: in createOrAssign"
        if self.lookahead.type in ff_sets.createOrAssign_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match_type('Id'):

                    print "createOrAssign -> Id"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: createOrAssign(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.createOrAssign_FOLLOW:
            print "createOrAssign -> EPSILON"
            return True
        else:
            return False

    def varDeclTail(self):
        print "Syntactical_Parser: in varDeclTail"
        if self.lookahead.value in ff_sets.varDeclTail_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.indice() and self.is_Assign() and self.match(';'):

                    print "varDeclTail -> indice is_Assign ;"

                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: varDeclTail(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def is_Assign(self):
        print "Syntactical_Parser: in is_Assign"
        if self.lookahead.value in ff_sets.is_Assign_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.assignOp() and self.expr():

                    print "is_Assign -> assignOp expr"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: is_Assign(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.is_Assign_FOLLOW:
            print "is_Assign -> EPSILON"
            return True
        else:
            return False

    def statement(self):
        print "Syntactical_Parser: in statement"
        if self.lookahead.value in ff_sets.statement_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('for') and self.match('(') and self.type() and self.match_type(
                        'Id') and self.assignOp() and self.expr() and self.match(';') and self.relExpr() and self.match(
                        ';') and self.assignStat() and self.match(')') and self.statBlock() and self.match(';'):
                    print "statement -> for ( type Id assignOp expr ; relExpr ; assignStat ) statBlock ;"
                    #
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: statement(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()

        elif self.lookahead.value in ff_sets.statement_FIRST2:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('if') and self.match('(') and self.expr() and self.match(')') and self.match(
                        'then') and self.statBlock() and self.match('else') and self.statBlock() and self.match(';'):

                    print "statement -> if ( expr ) then statBlock else statBlock ;"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: statement(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()

        elif self.lookahead.value in ff_sets.statement_FIRST3:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('get') and self.match('(') and self.variable() and self.match(')') and self.match(';'):
                    print "statement -> get ( variable ) ;"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: statement(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()

        elif self.lookahead.value in ff_sets.statement_FIRST4:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('put') and self.match('(') and self.expr() and self.match(')') and self.match(';'):
                    print "statement -> put ( expr ) ;"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: statement(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()

        elif self.lookahead.value in ff_sets.statement_FIRST5:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('return') and self.match('(') and self.expr() and self.match(')') and self.match(';'):
                    print "statement -> return ( expr ) ;"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: statement(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()

        elif self.lookahead.value in ff_sets.statement_FIRST6 or self.is_type_Id():  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.varDecl():
                    print "statement -> varDecl"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: statement(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()

        else:
            return False

    def gen_statements(self):
        print "Syntactical_Parser: in gen_statements"
        if self.lookahead.value in ff_sets.gen_statements_FIRST1 or self.is_type_Id():  # LHS-RHS1

            while self.lookahead.type != '$':
                if self.statement() and self.gen_statements():

                    print "gen_statements -> statement gen_statements"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: gen_statements(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.gen_statements_FOLLOW:
            print "gen_statements -> EPSILON"
            return True
        else:
            return False

    def assignStat(self):
        print "Syntactical_Parser: in assignStat"
        if self.lookahead.type in ff_sets.assignStat_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.variable() and self.assignOp() and self.expr():

                    print "assignStat -> variable assignOp expr"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: assignStat(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def statBlock(self):
        print "Syntactical_Parser: in statBlock"
        if self.lookahead.value in ff_sets.statBlock_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('{') and self.gen_statements() and self.match('}'):

                    print "statBlock -> { gen_statements }"

                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: statBlock(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.statBlock_FIRST2 or self.is_type_Id():  # LHS-RHS2
            while self.lookahead.type != '$':
                if self.statement():

                    print "statBlock -> statement"

                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: statBlock(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()

        elif self.lookahead.value in ff_sets.statBlock_FOLLOW:
            print "statBlock -> EPSILON"
            return True
        else:
            return False

    def expr(self):
        print "Syntactical_Parser: in expr"
        if self.lookahead.value in ff_sets.expr_FIRST1 or self.lookahead.type in ff_sets.expr_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.arithExpr() and self.gen_relArithExpr():

                    print "expr -> arithExpr gen_relArithExpr"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: expr(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def relExpr(self):
        print "Syntactical_Parser: in relExpr"
        if self.lookahead.value in ff_sets.relExpr_FIRST1 or self.is_type_Id():  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.arithExpr() and self.relOp() and self.arithExpr():

                    print "relExpr -> arithExpr relOp arithExpr"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: relExpr(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def gen_relArithExpr(self):
        print "Syntactical_Parser: in gen_relArithExpr"
        if self.lookahead.value in ff_sets.gen_relArithExpr_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.relOp() and self.arithExpr():

                    print "gen_relArithExpr -> relOp arithExpr"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: gen_relArithExpr(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.gen_relArithExpr_FOLLOW:
            print "gen_relArithExpr -> EPSILON"
            return True
        else:
            return False

    def arithExpr(self):
        print "Syntactical_Parser: in arithExpr"
        if self.lookahead.value in ff_sets.arithExpr_FIRST1 or self.lookahead.type in ff_sets.arithExpr_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.term() and self.gen_addArithExpr():

                    print "arithExpr -> term gen_addArithExpr"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: arithExpr(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def gen_addArithExpr(self):
        print "Syntactical_Parser: in gen_addArithExpr"
        if self.lookahead.value in ff_sets.gen_addArithExpr_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.addOp() and self.arithExpr():

                    print "gen_addArithExpr -> addOp arithExpr"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: gen_addArithExpr(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.gen_addArithExpr_FOLLOW:
            print "gen_addArithExpr -> EPSILON"
            return True
        else:
            return False

    def sign(self):
        print "Syntactical_Parser: in sign"
        if self.lookahead.value in ff_sets.sign_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('+'):

                    print "sign -> +"
                    return True
                elif self.match('-'):

                    print "sign -> -"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: sign(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def term(self):
        print "Syntactical_Parser: in term"
        if self.lookahead.value in ff_sets.term_FIRST1 or self.lookahead.type in ff_sets.term_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.factor() and self.gen_Term():

                    print "term -> factor gen_Term"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: term(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def gen_Term(self):
        print "Syntactical_Parser: in gen_Term"
        if self.lookahead.value in ff_sets.gen_Term_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.multOp() and self.term():

                    print "gen_Term -> multOp term"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: gen_Term(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.gen_Term_FOLLOW:
            print "gen_Term -> EPSILON"
            return True
        else:
            return False

    def factor(self):
        print "Syntactical_Parser: in factor"
        if self.lookahead.type in ff_sets.factor_FIRST1:
            while self.lookahead.type != '$':
                if self.match_type('Id') and self.paramsOrIndice():

                    print "factor -> Id paramsOrIndice"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: factor(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.factor_FIRST2:
            while self.lookahead.type != '$':
                if self.match('(') and self.arithExpr() and self.match(')'):

                    print "factor -> ( arithExpr )"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: factor(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.factor_FIRST3:
            while self.lookahead.type != '$':
                if self.match('not') and self.factor():

                    print "factor -> not factor"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: factor(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.type in ff_sets.factor_FIRST4:
            while self.lookahead.type != '$':
                if self.match_type('int'):

                    print "factor -> int"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: factor(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.type in ff_sets.factor_FIRST5:
            while self.lookahead.type != '$':
                if self.match_type('float'):

                    print "factor -> float"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: factor(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.factor_FIRST6:
            while self.lookahead.type != '$':
                if self.sign() and self.factor():

                    print "factor -> sign factor"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: factor(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def paramsOrIndice(self):
        print "Syntactical_Parser: in paramsOrIndice"
        if self.lookahead.value in ff_sets.paramsOrIndice_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('(') and self.aParams() and self.match(')'):

                    print "paramsOrIndice -> ( aParams )"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: paramsOrIndice(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()

        if self.indice():

            print "paramsOrIndice -> indice"
            return True
        else:
            return False

    def variable(self):
        print "Syntactical_Parser: in variable"

        if self.match_type('Id') and self.indice():

            print "variable -> Id indice"
            return True
        else:
            return False

    def indice(self):
        print "Syntactical_Parser: in indice"
        if self.lookahead.value in ff_sets.indice_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('[') and self.arithExpr() and self.match(']') and self.indice():

                    print "indice -> [ arithExpr ] indice"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: indice(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value == '.':  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('.') and self.match_type('Id') and self.paramsOrIndice():

                    print "indice -> . Id paramsOrIndice"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: indice(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.indice_FOLLOW:
            print "indice -> EPSILON"
            return True
        else:
            return False

    def arraySize(self):
        print "Syntactical_Parser: in arraySize"
        if self.lookahead.value in ff_sets.arraySize_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('[') and self.match_type('int') and self.match(']'):

                    print "arraySize -> [ int ]"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: arraySize(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.arraySize_FOLLOW:
            print "arraySize -> EPSILON"
            return True
        else:
            return False

    def type(self):
        print "Syntactical_Parser: in type"
        if self.lookahead.value in ff_sets.fParams_FIRST1 or self.is_type_Id():  # LHS-RHS1
            if self.match_type('Id'):

                print "type -> Id"
                return True
            elif self.match('int'):

                print "type -> int"
                return True
            elif self.match('float'):

                print "type -> float"
                return True
        else:
            return False

    def P_Type(self):
        print "Syntactical_Parser: in P_Type"
        if self.lookahead.value in ff_sets.P_Type_FIRST1:  # LHS-RHS1
            if self.match('int'):

                print "type -> int"
                return True
            elif self.match('float'):

                print "type -> float"
                return True
        else:
            return False

    def UD_Type(self):
        print "Syntactical_Parser: in UD_Type"
        if self.lookahead.type in ff_sets.UD_Type_FIRST1:  # LHS-RHS1
            if self.match_type('Id'):

                print "type -> Id"
                return True
        else:
            return False

    def fParams(self):
        print "Syntactical_Parser: in fParams"
        if self.lookahead.value in ff_sets.fParams_FIRST1 or self.is_type_Id():  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.type() and self.match_type('Id') and self.arraySize() and self.fParamsTail():

                    print "fParams -> type Id arraySize fParamsTail"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: fParams(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.fParams_FOLLOW:
            print "fParams -> EPSILON"
            return True
        else:
            return False

    def aParams(self):
        print "Syntactical_Parser: in aParams"
        if self.lookahead.value in ff_sets.aParams_FIRST1 or self.is_type_Id():  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.expr() and self.aParamsTail():

                    print "aParams -> expr aParamsTail"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: aParams(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value == ')':
            print "fParamsTail -> EPSILON"
            return True
        else:
            return False

    def fParamsTail(self):
        print "Syntactical_Parser: in fParamsTail"
        if self.lookahead.value in ff_sets.fParamsTail_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match(',') and self.type() and self.match_type('Id') and self.arraySize() and self.fParamsTail():

                    print "fParamsTail -> , type Id arraySize fParamsTail"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: fParamsTail(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.fParamsTail_FOLLOW:
            print "fParamsTail -> EPSILON"
            return True
        else:
            return False

    def aParamsTail(self):
        print "Syntactical_Parser: in aParamsTail"
        if self.lookahead.value in ff_sets.aParamsTail_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match(',') and self.expr() and self.aParamsTail():

                    print "aParamsTail -> , expr aParamsTail"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: aParamsTail(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        elif self.lookahead.value in ff_sets.aParamsTail_FOLLOW:
            print "aParamsTail -> EPSILON"
            return True
        else:
            return False

    def assignOp(self):
        print "Syntactical_Parser: in assignOp"
        if self.lookahead.value in ff_sets.assignOp_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('='):

                    print "assignOp -> ="
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: assignOp(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def relOp(self):
        print "Syntactical_Parser: in relOp"
        if self.lookahead.value in ff_sets.relOp_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('<') or self.match('<=') or self.match('<>') or self.match('==') or self.match('>') or self.match('>='):

                    print "relOp -> < | <= | <> | == | > | >="
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: relOp(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def addOp(self):
        print "Syntactical_Parser: in addOp"
        if self.lookahead.value in ff_sets.addOp_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('+') or self.match('-') or self.match('or'):

                    print "addOp -> + | - | or"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: addOp(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def multOp(self):
        print "Syntactical_Parser: in multOp"
        if self.lookahead.value in ff_sets.multOp_FIRST1:  # LHS-RHS1
            while self.lookahead.type != '$':
                if self.match('*') or self.match('/') or self.match('and'):

                    print "multOp -> * | / | and"
                    return True
                else:

                    self.err_token = self.lookahead.value
                    self.output += '\n~err in: multOp(): ' + self.err_token + '\n'
                    self.lookahead = self.interpreter.scanner()
        else:
            return False

    def prettify_output(self):
        # self.o = open(self.outfile, 'rw+')
        scope = 0
        tabs = ''
        newline = False
        for c in self.output:

            while self.lookahead.type != '$':
                if c == '}':
                    tabs = tabs[:-4]

                elif c == '{':
                    tabs += '    '
                    c = '{\n'


if __name__ == '__main__':
    parser = Syntactic_Parser()
    parser.parse()
