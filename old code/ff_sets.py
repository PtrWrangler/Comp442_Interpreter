prog_FIRST1 = ['class', 'program']
classDecl_FIRST1 = ['class']
classDecl_FOLLOW = ['program']
classBody_FIRST1 = ['Id', 'float', 'int']
classBody_FOLLOW = ['}']
varOrFunc_FIRST1 = ['[', ';', '.']
varOrFunc_FIRST2 = ['(']
progBody_FIRST1 = ['program']
funcHead_FIRST1 = ['Id', 'float', 'int']
funcDef_FIRST1 = ['Id', 'float', 'int']
funcDef_FOLLOW = ['$']
funcBody_FIRST1 = ['{']
varDecl_FIRST1 = ['Id']
varDecl_FIRST2 = ['float', 'int']
createOrAssign_FIRST1 = ['Id']
createOrAssign_FOLLOW = ['[', '=', ';', '.']
varDeclTail_FIRST1 = ['[', '=', ';', '.']
is_Assign_FIRST1 = ['=']
is_Assign_FOLLOW = [';']
statement_FIRST1 = ['for']
statement_FIRST2 = ['if']
statement_FIRST3 = ['get']
statement_FIRST4 = ['put']
statement_FIRST5 = ['return']
statement_FIRST6 = ['Id', 'float', 'int']
gen_statements_FIRST1 = ['for', 'if', 'get', 'put', 'return', 'Id', 'float', 'int']
gen_statements_FOLLOW = ['}']
assignStat_FIRST1 = ['Id']
statBlock_FIRST1 = ['{']
statBlock_FIRST2 = ['for', 'if', 'get', 'put', 'return', 'Id', 'float', 'int']
statBlock_FOLLOW = [';', 'else']
expr_FIRST1 = ['(', 'Id', 'float', 'int', 'not', '+', '-']
relExpr_FIRST1 = ['(', 'Id', 'float', 'int', 'not', '+', '-']
gen_relArithExpr_FIRST1 = ['<', '<=', '<>', '==', '>', '>=']
gen_relArithExpr_FOLLOW = [';', ')', ',']
arithExpr_FIRST1 = ['(', 'Id', 'float', 'int', 'not', '+', '-']
gen_addArithExpr_FIRST1 = ['+', '-', 'or']
gen_addArithExpr_FOLLOW = [';', ')', ',', '<', '<=', '<>', '==', '>', '>=', ']']
sign_FIRST1 = ['+', '-']
term_FIRST1 = ['(', 'Id', 'float', 'int', 'not', '+', '-']
gen_Term_FIRST1 = ['*', '/', 'and']
gen_Term_FOLLOW = [';', ')', ',', '<', '<=', '<>', '==', '>', '>=', ']', '+', '-', 'or']
factor_FIRST1 = ['Id']
factor_FIRST2 = ['(']
factor_FIRST3 = ['not']
factor_FIRST4 = ['int']
factor_FIRST5 = ['float']
factor_FIRST6 = ['+', '-']
paramsOrIndice_FIRST1 = ['(']
paramsOrIndice_FIRST2 = ['[', '.']
paramsOrIndice_FOLLOW = [';', ')', ',', '<', '<=', '<>', '==', '>', '>=', ']', '+', '-', 'or', '*', '/', 'and']
variable_FIRST1 = ['Id']
indice_FIRST1 = ['[']
indice_FOLLOW = [';', ')', ',', '<', '<=', '<>', '==', '>', '>=', ']', '+', '-', 'or', '*', '/', 'and', '=']
arraySize_FIRST1 = ['[']
arraySize_FOLLOW = [')', ',']
type_FIRST1 = ['Id', 'int', 'float']
P_Type_FIRST1 = ['int', 'float']
UD_Type_FIRST1 = ['Id']
fParams_FIRST1 = ['Id', 'float', 'int']
fParams_FOLLOW = [')']
aParams_FIRST1 = ['(', 'Id', 'float', 'int', 'not', '+', '-']
fParamsTail_FIRST1 = [',']
fParamsTail_FOLLOW = [')']
aParamsTail_FIRST1 = [',']
aParamsTail_FOLLOW = [')']
assignOp_FIRST1 = ['=']
relOp_FIRST1 = ['>=', '>', '==', '<>', '<=', '<']
addOp_FIRST1 = ['+', '-', 'or']
multOp_FIRST1 = ['*', '/', 'and']
