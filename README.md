# Comp442_Interpreter

COMP 442 Winter 2017 Assignment 4, Symantic Analysis
By: Mathieu Rauch
ID: 26777147

----------------------------------------------------------------------------

Installation and preparation instructions:

To Run you need python ~v2.7
(I actually experimented with a pypy compiler to make things more interesting with it’s JIT compiler)
    (also compatible: pypy2-v5.6)

Execution Instructions:

from your terminal execute the command in the unpacked root project folder:
    python TableParser.py
If you want to change the input testfile (source program),
    open TableParser.py with your any text editor and specify the testFile name and dir at the top
sample testfiles are in /testing and all outputs and errorlogs are sent to /output


----------------------------------------------------------------------------

--- Important Notes ---
- I have now upgraded to a Table-Driven Predictive Parser (RDPP).
- To see the symbol_tables and entries printout your source code must be error free
    a good file to use would be 'test_Utility.txt'
- The semantic tables and their entries can be found at the bottom of the respective test's output file file
    a good sample can be found in 'Outputs/Utility_Outs~Errs.txt'


--- Description of Semantic Processing and Semantic Rules added ---
- Semantic Processing is done in the SemnaticProcessor.py file. it is created in the TableParser.py file and used when a semantic token is encountered in the grammar.

CREATE_GLOBAL_TABLE
    simply creates the initial global table, and puts it at the bottom of the SemanticTable_stack.

CLASS_ENTRY_TABLE
    Creates a class entry in the global table and a new semantic table for the class.
    Point the class' entry link variable to the new semantic table.
    increment the scope level variable
    Push the class semantic table on the SemanticTable_stack to keep track of scope for later.

END_CLASS
    Pops the class semantic table off the semantic stack and
    decrements the scope level variable

ENTRY_TYPE
    A variable or function declaration is starting, make sure the attr_stack is clear.
    Then push the type on the attr stack for migration until the entry is ready.

ENTRY_NAME
    The identifier of a variable or function declaration is scanned.
    Push it on the attr_stack for migration until the entry is ready.

ADD_DECL_ARRAY_DIM
    If the variable or function parameter that you are processing is an array,
    for each dimension, push the arraySize on the attr_stack for migration until the entry is ready

FUNC_ENTRY_TABLE
    pop the attr_stack's migrated attrs for the function and create the function entry
    link this entry to a newly created symbol table for this function.
    Increment the scope level

ADD_FUNC_PARAM_ENTRY
    create a new parameter in the function table with the migrated variable attributes in the attr_stack.
    You also go back one table to the entry of the function to add the parameter in the type information section.

END_FUNC
    Much like ending a class, you just pop the semantic table off the semantic table stack.
    decrement the scope level variable.

VAR_ENTRY
    pop the attr_stack's migrated attrs for the function and create the function entry
    link this entry to a newly created symbol table for this function.
    Increment the scope level


--- Description/rationale of the overall structure of the solution ---
TABLE PARSING:
- The TableParser class implements Table Predictive Parsing and calls the Lexer for next tokens. To start the TableParser builds the grammar object filled with all the productions and each of their RHS objects containing their first and possible follow sets. Then the parser gets a list of all possible Lexical tokens from the lexical analyzer's specifications. Then using an algorithm it creates the parsing table from the grammar dictionary and the terminals list.

SEMANTIC ANALYZING:
- The SemanticProcessor object is initialised before the table predictive parser starts parsing. It already knows all the possible incoming semantic symbols contained in the grammar inside of a dispatcher dictionary. The semantic processor buffers a single terminal symbol each time one is parsed to be able to act on it if a semantic action comes next. When a semantic symbol is encountered on the parsing stack it calls the semantic_processor's dispatcher dictionary's corresponding function to execute the desired semantic command. The programs variable and function declarations are most likely spread over multiple grammatical rules, requiring us to perform attribute migration. The semantic processor does this by pushing declaration types, ids, arraySizes and function parameters on a attr_stack and popping them off in the correct order when it comes time create a full variable/function entry/table.
- The whole semantic analysis procedure relies on the fact that there are no parsing errors. If there is even one parsing error than all the semantic tables and entries are unreliable. If there are no parsing errors, then at the end of the parsing and semantic processing you will have accurate class/variable/function information.
- Assuming you have gotten this far with no errors you now call the global table to check for duplicate variable declarations, calling uninitialized variables and cyclic class dependency checking. This is done in the Symbol_Table object's IDUsageErrors() function.


--- Errors ---
- Errors are reported at the bottom of the debug output file log files.
- All error locations specified are accurate to the original input test file and not the debug output displayed above the errors
- The production function is also listed at the beginning of the error to help you understand what the parser is expecting.

!- My error recovery technique currently works to re syncronize both the parsing stack and the lookahead scanner to the closest generic/common sync_token expected in the parsing stack e.g. [';', '{', '}']


--- Description of method used to apply any changes to the my grammar. ---
- When I need to make changes to my grammar I have to revert to my version without the upgraded semantic symbols and make changes in KFGedit then place all the semantic symbols back in and make any changes to them if necessary. This method is very crude because then I need to read all the first and follow sets to update them in my specially formatted grammar+ first and follow set file by hand. when my program runs it reads from this specially formatted file and creates all the production objects for me to work with.


--- Other Notes ---
- List of changes and notes about the grammar can be found in
    'Grammar Notes/442 A2 grammar change notes.txt'

- My First and Follow sets can be found here along with the updated grammar.
    'Grammar Notes/PPT_Grammar+.txt'



--- Tools and Libraries used and Bibliography ---
- KFGedit was a great tool that I used to help me fix the grammar.
    It allowed me to understand what the first and follow sets really meant and understand how they relate to making a grammar LL(1).

- A lot of stack overflow...
- the slides
