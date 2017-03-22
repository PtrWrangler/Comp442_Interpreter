# Comp442_Interpreter

COMP 442 Winter 2017 Assignment 3, Symantic Analysis
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


--- Description of Semantic Processing and Semantic Rules added ---
- Semantic Processing is done in the SemnaticProcessor.py file. it is created in the TableParser.py file and used when a semantic token is encountered in the grammar.

[A-Z]+_

CREATE_GLOBAL_TABLE
    simply creates the initial global table, and puts it at the bottom of the SemanticTable_stack.

CLASS_ENTRY_TABLE
    Creates a class entry in the global table and a semantic table for the class.
    Point the class entries link variable to the new semantic table.
    Push the class semantic table on the SemanticTable_stack to keep track of scope for later.

END_CLASS
CLASS_FUNC_ENTRY_TABLE
END_CLASS_FUNC
CLASS_VAR_ENTRY
ENTRY_TYPE
ENTRY_NAME
ADD_DECL_ARRAY_DIM


--- Description of method used to apply any changes to the my grammar. ---
- When I need to make changes to my grammar I have to revert to my version without the upgraded semantic symbols and make changes in KFGedit then place all the semantic symbols back in and make any changes to them if necessary. This method is very crude because then I need to read all the first and follow sets to update them in my specially formatted grammar+first and follow set file by hand. when my program runs it reads from this specially formatted file and creates all the production objects for me to work with.


--- Description/rationale of the overall structure of the solution ---
- The Parser class implements recursive descent predictive parsing and calls the Lexer for next tokens. Since the RDPP method requires having a ton of functions for each production I created some tools to help me generate them and/or edit them. they are in the 'tools/' folder. Also, there is a tool to help me generate my first and follow sets when I change my grammar.


--- Errors ---
- Errors are reported at the bottom of the debug output file log files.
- All error locations specified are accurate to the original input test file and not the debug output displayed above the errors
- The production function is also listed at the beginning of the error to help you understand what the parser is expecting.

!- My error recovery technique currently works to re syncronize both the parsing stack and the lookahead scanner to the closest generic/common sync_token expected in the parsing stack e.g. [';', '{', '}']





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
