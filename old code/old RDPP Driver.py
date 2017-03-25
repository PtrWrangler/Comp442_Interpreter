from Lexer import Lexical_Analyzer, Token
from Lexer import SCAN_ERROR, EOF, reserved_words
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

    def prog(self):
        print 'Syntactical_Parser: in prog'
        if self.lookahead.value in ff_sets.prog_FIRST1 or self.lookahead.type in ff_sets.prog_FIRST1:
            while self.lookahead.type != '$':
                if self.progBody:

                print 'prog -> '
    def classDecl(self):
        print 'Syntactical_Parser: in classDecl'
        if self.lookahead.value in ff_sets.classDecl_FIRST1 or self.lookahead.type in ff_sets.classDecl_FIRST1:
            while self.lookahead.type != '$':
                if self.classDecl:

                print 'classDecl -> '
#classDecl_FOLLOW = 	follow: {program}
    def classBody(self):
        print 'Syntactical_Parser: in classBody'
        if self.lookahead.value in ff_sets.classBody_FIRST1 or self.lookahead.type in ff_sets.classBody_FIRST1:
            while self.lookahead.type != '$':
                if self.varOrFunc:

                print 'classBody -> '
#classBody_FOLLOW = 	follow: {}}
    def varOrFunc(self):
        print 'Syntactical_Parser: in varOrFunc'
        if self.lookahead.value in ff_sets.varOrFunc_FIRST1 or self.lookahead.type in ff_sets.varOrFunc_FIRST1:
            while self.lookahead.type != '$':
                if self.classBody:

                print 'varOrFunc -> '
        if self.lookahead.value in ff_sets.varOrFunc_FIRST1 or self.lookahead.type in ff_sets.varOrFunc_FIRST1:
            while self.lookahead.type != '$':
                if self.classBody:

                print 'varOrFunc -> '
    def progBody(self):
        print 'Syntactical_Parser: in progBody'
        if self.lookahead.value in ff_sets.progBody_FIRST1 or self.lookahead.type in ff_sets.progBody_FIRST1:
            while self.lookahead.type != '$':
                if self.funcDef:

                print 'progBody -> '
    def funcHead(self):
        print 'Syntactical_Parser: in funcHead'
        if self.lookahead.value in ff_sets.funcHead_FIRST1 or self.lookahead.type in ff_sets.funcHead_FIRST1:
            while self.lookahead.type != '$':
                if self.):

                print 'funcHead -> '
    def funcDef(self):
        print 'Syntactical_Parser: in funcDef'
        if self.lookahead.value in ff_sets.funcDef_FIRST1 or self.lookahead.type in ff_sets.funcDef_FIRST1:
            while self.lookahead.type != '$':
                if self.funcDef:

                print 'funcDef -> '
#funcDef_FOLLOW = 	follow: {$}
    def funcBody(self):
        print 'Syntactical_Parser: in funcBody'
        if self.lookahead.value in ff_sets.funcBody_FIRST1 or self.lookahead.type in ff_sets.funcBody_FIRST1:
            while self.lookahead.type != '$':
                if self.}:

                print 'funcBody -> '
    def varDecl(self):
        print 'Syntactical_Parser: in varDecl'
        if self.lookahead.value in ff_sets.varDecl_FIRST1 or self.lookahead.type in ff_sets.varDecl_FIRST1:
            while self.lookahead.type != '$':
                if self.varDeclTail:

                print 'varDecl -> '
        if self.lookahead.value in ff_sets.varDecl_FIRST1 or self.lookahead.type in ff_sets.varDecl_FIRST1:
            while self.lookahead.type != '$':
                if self.varDeclTail:

                print 'varDecl -> '
    def createOrAssign(self):
        print 'Syntactical_Parser: in createOrAssign'
        if self.lookahead.value in ff_sets.createOrAssign_FIRST1 or self.lookahead.type in ff_sets.createOrAssign_FIRST1:
            while self.lookahead.type != '$':
                if self.Id:

                print 'createOrAssign -> '
#createOrAssign_FOLLOW = 	follow: {[, =, ;, .}
    def varDeclTail(self):
        print 'Syntactical_Parser: in varDeclTail'
        if self.lookahead.value in ff_sets.varDeclTail_FIRST1 or self.lookahead.type in ff_sets.varDeclTail_FIRST1:
            while self.lookahead.type != '$':
                if self.;:

                print 'varDeclTail -> '
    def is_Assign(self):
        print 'Syntactical_Parser: in is_Assign'
        if self.lookahead.value in ff_sets.is_Assign_FIRST1 or self.lookahead.type in ff_sets.is_Assign_FIRST1:
            while self.lookahead.type != '$':
                if self.expr:

                print 'is_Assign -> '
#is_Assign_FOLLOW = 	follow: {;}
    def statement(self):
        print 'Syntactical_Parser: in statement'
        if self.lookahead.value in ff_sets.statement_FIRST1 or self.lookahead.type in ff_sets.statement_FIRST1:
            while self.lookahead.type != '$':
                if self.;:

                print 'statement -> '
        if self.lookahead.value in ff_sets.statement_FIRST1 or self.lookahead.type in ff_sets.statement_FIRST1:
            while self.lookahead.type != '$':
                if self.;:

                print 'statement -> '
        if self.lookahead.value in ff_sets.statement_FIRST1 or self.lookahead.type in ff_sets.statement_FIRST1:
            while self.lookahead.type != '$':
                if self.;:

                print 'statement -> '
        if self.lookahead.value in ff_sets.statement_FIRST1 or self.lookahead.type in ff_sets.statement_FIRST1:
            while self.lookahead.type != '$':
                if self.;:

                print 'statement -> '
        if self.lookahead.value in ff_sets.statement_FIRST1 or self.lookahead.type in ff_sets.statement_FIRST1:
            while self.lookahead.type != '$':
                if self.;:

                print 'statement -> '
        if self.lookahead.value in ff_sets.statement_FIRST1 or self.lookahead.type in ff_sets.statement_FIRST1:
            while self.lookahead.type != '$':
                if self.;:

                print 'statement -> '
    def gen_statements(self):
        print 'Syntactical_Parser: in gen_statements'
        if self.lookahead.value in ff_sets.gen_statements_FIRST1 or self.lookahead.type in ff_sets.gen_statements_FIRST1:
            while self.lookahead.type != '$':
                if self.gen_statements:

                print 'gen_statements -> '
#gen_statements_FOLLOW = 	follow: {}}
    def assignStat(self):
        print 'Syntactical_Parser: in assignStat'
        if self.lookahead.value in ff_sets.assignStat_FIRST1 or self.lookahead.type in ff_sets.assignStat_FIRST1:
            while self.lookahead.type != '$':
                if self.expr:

                print 'assignStat -> '
    def statBlock(self):
        print 'Syntactical_Parser: in statBlock'
        if self.lookahead.value in ff_sets.statBlock_FIRST1 or self.lookahead.type in ff_sets.statBlock_FIRST1:
            while self.lookahead.type != '$':
                if self.}:

                print 'statBlock -> '
        if self.lookahead.value in ff_sets.statBlock_FIRST1 or self.lookahead.type in ff_sets.statBlock_FIRST1:
            while self.lookahead.type != '$':
                if self.}:

                print 'statBlock -> '
#statBlock_FOLLOW = 	follow: {;, else}
    def expr(self):
        print 'Syntactical_Parser: in expr'
        if self.lookahead.value in ff_sets.expr_FIRST1 or self.lookahead.type in ff_sets.expr_FIRST1:
            while self.lookahead.type != '$':
                if self.gen_relArithExpr:

                print 'expr -> '
    def relExpr(self):
        print 'Syntactical_Parser: in relExpr'
        if self.lookahead.value in ff_sets.relExpr_FIRST1 or self.lookahead.type in ff_sets.relExpr_FIRST1:
            while self.lookahead.type != '$':
                if self.arithExpr:

                print 'relExpr -> '
    def gen_relArithExpr(self):
        print 'Syntactical_Parser: in gen_relArithExpr'
        if self.lookahead.value in ff_sets.gen_relArithExpr_FIRST1 or self.lookahead.type in ff_sets.gen_relArithExpr_FIRST1:
            while self.lookahead.type != '$':
                if self.arithExpr:

                print 'gen_relArithExpr -> '
#gen_relArithExpr_FOLLOW = 	follow: {;, ), ,}
    def arithExpr(self):
        print 'Syntactical_Parser: in arithExpr'
        if self.lookahead.value in ff_sets.arithExpr_FIRST1 or self.lookahead.type in ff_sets.arithExpr_FIRST1:
            while self.lookahead.type != '$':
                if self.gen_addArithExpr:

                print 'arithExpr -> '
    def gen_addArithExpr(self):
        print 'Syntactical_Parser: in gen_addArithExpr'
        if self.lookahead.value in ff_sets.gen_addArithExpr_FIRST1 or self.lookahead.type in ff_sets.gen_addArithExpr_FIRST1:
            while self.lookahead.type != '$':
                if self.arithExpr:

                print 'gen_addArithExpr -> '
#gen_addArithExpr_FOLLOW = 	follow: {;, ), ,, <, <=, <>, ==, >, >=, ]}
    def sign(self):
        print 'Syntactical_Parser: in sign'
        if self.lookahead.value in ff_sets.sign_FIRST1 or self.lookahead.type in ff_sets.sign_FIRST1:
            while self.lookahead.type != '$':
                if self.-:

                print 'sign -> '
    def term(self):
        print 'Syntactical_Parser: in term'
        if self.lookahead.value in ff_sets.term_FIRST1 or self.lookahead.type in ff_sets.term_FIRST1:
            while self.lookahead.type != '$':
                if self.gen_Term:

                print 'term -> '
    def gen_Term(self):
        print 'Syntactical_Parser: in gen_Term'
        if self.lookahead.value in ff_sets.gen_Term_FIRST1 or self.lookahead.type in ff_sets.gen_Term_FIRST1:
            while self.lookahead.type != '$':
                if self.term:

                print 'gen_Term -> '
#gen_Term_FOLLOW = 	follow: {;, ), ,, <, <=, <>, ==, >, >=, ], +, -, or}
    def factor(self):
        print 'Syntactical_Parser: in factor'
        if self.lookahead.value in ff_sets.factor_FIRST1 or self.lookahead.type in ff_sets.factor_FIRST1:
            while self.lookahead.type != '$':
                if self.paramsOrIndice:

                print 'factor -> '
        if self.lookahead.value in ff_sets.factor_FIRST1 or self.lookahead.type in ff_sets.factor_FIRST1:
            while self.lookahead.type != '$':
                if self.paramsOrIndice:

                print 'factor -> '
        if self.lookahead.value in ff_sets.factor_FIRST1 or self.lookahead.type in ff_sets.factor_FIRST1:
            while self.lookahead.type != '$':
                if self.paramsOrIndice:

                print 'factor -> '
        if self.lookahead.value in ff_sets.factor_FIRST1 or self.lookahead.type in ff_sets.factor_FIRST1:
            while self.lookahead.type != '$':
                if self.paramsOrIndice:

                print 'factor -> '
        if self.lookahead.value in ff_sets.factor_FIRST1 or self.lookahead.type in ff_sets.factor_FIRST1:
            while self.lookahead.type != '$':
                if self.paramsOrIndice:

                print 'factor -> '
        if self.lookahead.value in ff_sets.factor_FIRST1 or self.lookahead.type in ff_sets.factor_FIRST1:
            while self.lookahead.type != '$':
                if self.paramsOrIndice:

                print 'factor -> '
    def paramsOrIndice(self):
        print 'Syntactical_Parser: in paramsOrIndice'
        if self.lookahead.value in ff_sets.paramsOrIndice_FIRST1 or self.lookahead.type in ff_sets.paramsOrIndice_FIRST1:
            while self.lookahead.type != '$':
                if self.indice:

                print 'paramsOrIndice -> '
        if self.lookahead.value in ff_sets.paramsOrIndice_FIRST1 or self.lookahead.type in ff_sets.paramsOrIndice_FIRST1:
            while self.lookahead.type != '$':
                if self.indice:

                print 'paramsOrIndice -> '
#paramsOrIndice_FOLLOW = 	follow: {;, ), ,, <, <=, <>, ==, >, >=, ], +, -, or, *, /, and}
    def variable(self):
        print 'Syntactical_Parser: in variable'
        if self.lookahead.value in ff_sets.variable_FIRST1 or self.lookahead.type in ff_sets.variable_FIRST1:
            while self.lookahead.type != '$':
                if self.indice:

                print 'variable -> '
    def indice(self):
        print 'Syntactical_Parser: in indice'
        if self.lookahead.value in ff_sets.indice_FIRST1 or self.lookahead.type in ff_sets.indice_FIRST1:
            while self.lookahead.type != '$':
                if self.indice:

                print 'indice -> '
#indice_FOLLOW = 	follow: {;, ), ,, <, <=, <>, ==, >, >=, ], +, -, or, *, /, and, =}
    def arraySize(self):
        print 'Syntactical_Parser: in arraySize'
        if self.lookahead.value in ff_sets.arraySize_FIRST1 or self.lookahead.type in ff_sets.arraySize_FIRST1:
            while self.lookahead.type != '$':
                if self.]:

                print 'arraySize -> '
#arraySize_FOLLOW = 	follow: {), ,}
    def type(self):
        print 'Syntactical_Parser: in type'
        if self.lookahead.value in ff_sets.type_FIRST1 or self.lookahead.type in ff_sets.type_FIRST1:
            while self.lookahead.type != '$':
                if self.float:

                print 'type -> '
    def P_Type(self):
        print 'Syntactical_Parser: in P_Type'
        if self.lookahead.value in ff_sets.P_Type_FIRST1 or self.lookahead.type in ff_sets.P_Type_FIRST1:
            while self.lookahead.type != '$':
                if self.float:

                print 'P_Type -> '
    def UD_Type(self):
        print 'Syntactical_Parser: in UD_Type'
        if self.lookahead.value in ff_sets.UD_Type_FIRST1 or self.lookahead.type in ff_sets.UD_Type_FIRST1:
            while self.lookahead.type != '$':
                if self.Id:

                print 'UD_Type -> '
    def fParams(self):
        print 'Syntactical_Parser: in fParams'
        if self.lookahead.value in ff_sets.fParams_FIRST1 or self.lookahead.type in ff_sets.fParams_FIRST1:
            while self.lookahead.type != '$':
                if self.fParamsTail:

                print 'fParams -> '
#fParams_FOLLOW = 	follow: {)}
    def aParams(self):
        print 'Syntactical_Parser: in aParams'
        if self.lookahead.value in ff_sets.aParams_FIRST1 or self.lookahead.type in ff_sets.aParams_FIRST1:
            while self.lookahead.type != '$':
                if self.aParamsTail:

                print 'aParams -> '
    def fParamsTail(self):
        print 'Syntactical_Parser: in fParamsTail'
        if self.lookahead.value in ff_sets.fParamsTail_FIRST1 or self.lookahead.type in ff_sets.fParamsTail_FIRST1:
            while self.lookahead.type != '$':
                if self.fParamsTail:

                print 'fParamsTail -> '
#fParamsTail_FOLLOW = 	follow: {)}
    def aParamsTail(self):
        print 'Syntactical_Parser: in aParamsTail'
        if self.lookahead.value in ff_sets.aParamsTail_FIRST1 or self.lookahead.type in ff_sets.aParamsTail_FIRST1:
            while self.lookahead.type != '$':
                if self.aParamsTail:

                print 'aParamsTail -> '
#aParamsTail_FOLLOW = 	follow: {)}
    def assignOp(self):
        print 'Syntactical_Parser: in assignOp'
        if self.lookahead.value in ff_sets.assignOp_FIRST1 or self.lookahead.type in ff_sets.assignOp_FIRST1:
            while self.lookahead.type != '$':
                if self.=:

                print 'assignOp -> '
    def relOp(self):
        print 'Syntactical_Parser: in relOp'
        if self.lookahead.value in ff_sets.relOp_FIRST1 or self.lookahead.type in ff_sets.relOp_FIRST1:
            while self.lookahead.type != '$':
                if self.>=:

                print 'relOp -> '
    def addOp(self):
        print 'Syntactical_Parser: in addOp'
        if self.lookahead.value in ff_sets.addOp_FIRST1 or self.lookahead.type in ff_sets.addOp_FIRST1:
            while self.lookahead.type != '$':
                if self.or:

                print 'addOp -> '
    def multOp(self):
        print 'Syntactical_Parser: in multOp'
        if self.lookahead.value in ff_sets.multOp_FIRST1 or self.lookahead.type in ff_sets.multOp_FIRST1:
            while self.lookahead.type != '$':
                if self.and:

                print 'multOp -> '
