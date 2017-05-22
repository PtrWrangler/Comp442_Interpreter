# Comp442_Interpreter
Language: MR--


     ______  _______        _____
    |      \/       \   ___|\    \
   /          /\     \ |    |\    \
  /     /\   / /\     ||    | |    |
 /     /\ \_/ / /    /||    |/____/      _____   _____
|     |  \|_|/ /    / ||    |\    \     (____/  (____/
|     |       |    |  ||    | |    |
|\____\       |____|  /|____| |____|
| |    |      |    | / |    | |    |
 \|____|      |____|/  |____| |____|
    \(          )/       \(     )/
     '          '         '     '

COMP 442 Winter 2017 Assignment 4, Semantic Verification and Code Generation
By: Mathieu Rauch
ID: 26777147

Repository:
https://github.com/PtrWrangler/Comp442_Interpreter/tree/master

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
- WORK_LOG.txt is now obsolete, now refer to the github repo to see the specific history of work that was done or navigate to TODO.txt
    to see tasks that has been accomplished or you can always check the READ_ME.md

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
    check if class name already exists.
    create a key (if one does not already exist in the classEntryDict for the class.

END_CLASS
    Pops the class semantic table off the semantic stack and
    decrements the scope level variable

ENTRY_TYPE
    A variable or function declaration is starting, make sure the attr_stack is clear.
    Also ensure indice_lists is clear.
    Then push the type on the attr stack for migration until the entry is ready.

ENTRY_NAME
    The identifier of a variable or function declaration is scanned.
    Push it on the attr_stack for migration until the entry is ready.

ADD_DECL_ARRAY
    If the variable or function parameter that you are processing is an array,
    for each dimension, push the arraySize on the attr_stack for migration until the entry is ready

FUNC_ENTRY_TABLE
    pop the attr_stack's migrated attrs for the function and create the function entry.
    link this entry to a newly created symbol table for this function.
    Increment the scope level.
    create a key (if one does not already exist in the classEntryDict for the class.


ADD_FUNC_PARAM_ENTRY
    create a new parameter in the function table with the migrated variable attributes in the attr_stack.
    You also go back one table to the entry of the function to add the parameter in the type information section.
    Check if variable name exists in scope

END_FUNC
    Much like ending a class, you just pop the semantic table off the semantic table stack.
    decrement the scope level variable.

VAR_ENTRY
    pop the attr_stack's migrated attrs for the function and create the function entry

    if type is UserDefined, check if it is really. Then place it in the classUsageDict for circular reference checking in the second pass.

    link this entry to a newly created symbol table for this function.
    Increment the scope level

PROGRAM_FUNC_ENTRY_TABLE
    Create the special program function in the global SymbolTable

APPEND_OP
    Used in expressions to append any operators or operands into the special stack of lists mechanism indice_lists.
    append to the top list of the indice_lists

START_IDX_DIM
    when starting an index for a factor in an expression, you have just created an entry at the end of the top list in indice_lists. so now to prepare to evaluate its indice Arithexpression you append another list on to the stack, that will eventually be packed up and placed in that you created below it entry below it.

END_IDX_DIM
    Now you are finished the arithexpression that is within the index fo a var entry. So pop that top list from the indice_lists stack and append it to the index parameter of the entry you had created below it.

FACTOR_ID
    when an operand of an expression is a variable/function call identifier, append a new entry at the end of the top list in the indice_lists stack

CHECK_VAR_EXIST
    check if the identifier has been declared for use in current scope

ASSIGNMENT_VAR
    create the variable entry and push it to wait for the evaluation of the expression following the '='

FINISH_ASSIGNMENT
    End of an assignment, take the expression and append it to the assignment parameter of the entry.

FUNC_CALL
    similarly to variable calls occuring in expression, when a function call occurs push a new list onto the indice_lists mechanism to handle the function call.

ADD_PARAM
    another param is incoming, push another indice_list on the stack

SAVE_PARAM
    param is finished, pop it and append it to the function call entries' IDXorPARAM attribute

END_FUNC_CALL
    pop any empty lists that may be on the top of the indice list.

END_PROGRAM
    Pops the program function semantic table off the semantic stack
    starts 'second pass' to check for proper existing UD_Type declaration and
    circular class dependency
    Validate proper return values of all functions.
    Expression typechecking of all indices and function params and assignment vars.

--- Description/rationale of the overall structure of the solution ---
TABLE PARSING:
- The TableParser class implements Table Predictive Parsing and calls the Lexer for next tokens. To start the TableParser builds the grammar object filled with all the productions and each of their RHS objects containing their first and possible follow sets. Then the parser gets a list of all possible Lexical tokens from the lexical analyzer's specifications. Then using an algorithm it creates the parsing table from the grammar dictionary and the terminals list.

SEMANTIC ANALYZING:
- The SemanticProcessor object is initialised before the table predictive parser starts parsing. It already knows all the possible incoming semantic symbols contained in the grammar inside of a dispatcher dictionary. The semantic processor buffers a single terminal symbol each time one is parsed to be able to act on it if a semantic action comes next. When a semantic symbol is encountered on the parsing stack it calls the semantic_processor's dispatcher dictionary's corresponding function to execute the desired semantic command. The programs variable and function declarations are most likely spread over multiple grammatical rules, requiring us to perform attribute migration. The semantic processor does this by pushing declaration types, ids, arraySizes and function parameters on a attr_stack and popping them off in the correct order when it comes time create a full variable/function entry/table.
- The whole semantic analysis procedure relies on the fact that there are no parsing errors. If there is even one parsing error than all the semantic tables and entries are unreliable. If there are no parsing errors, then at the end of the parsing and semantic processing you will have accurate class/variable/function information.
- Assuming you have gotten this far with no errors you now call the global table to check for duplicate variable declarations, calling uninitialized variables and cyclic class dependency checking. This is done in the Symbol_Table object's IDUsageErrors() function.

Specific Future Semantic Details:
     - The program does not process operations on entire arrays yet.
     - An expression longer than 1 factor can contain a mixture of floats and ints strictly but if you want to put a user defined type in an expression it must be the only factor. There are no operations that can be performed on objects yet relative or mathematical.
     - relative operators evaluate an expression to 1 or 0 (boolean as an int) -> so the presence of an relative operator forces return type to be int.
     index values note:
        float index will be allowed and will be concatenated at runtime into ints
        objects as indexes are not allowed
    assigning a float to an int variable will ust concatenate it too

     - Parameters will be passed to functions by reference. Im my experience it is a lot more useful to pass by reference and is a feature you would want your programming langauge to have. If you absolutely want you could simply make a deep copy of the reference in a new address.
     - There is no limit to the amount of parameters you can pass to your function but, in common practice if you are passing more than a handful of parameters to a function you're probably doing something inneficiently/unclearly in your code.
     - Right now, the way I have my language configured, you would not be able to overload functions because each function needs to have a unique name identifier.
     - Right now there is no plans for implementing recursion, I have yet to wrap my head around how that would function.
     - In the distant future potentially two instances of the same function could be active at the same time if the program is made to handle multiple threads. syncronizing the access to the subject addresses to prevent data races.

--- SymbolTable Schema ---
It is important to establish the description of how the symbol tables and their relationship to the entries are set up.

 Symbol Tables:
        - has a name and a list to store its respective entries that will be in its scope.

 Entries:
        - If the entry is a function or a class then it will make use of the link attr, which references the SymbolTable inside scope.
        - have fields to store name and type tokens which contain the original location to be able to reference
         should there be an error.
        - kind field will remember if the entry is a assignment/variable/function/variable call/function call/parameter/nest
        - arraySize for array declaration size
        - IDXorPARAMS to store either array index or in the case of a function the parameters being passed
        - memory location and assembly code alias are prepared to store their respective information.

--- ATTRIBUTE MIGRATION ---

The simple mechanism used for attribute migration in such things as the beginnings of variable/function declarations is basically using the attribute stack. as the type and identifier pass by I stack them as Token objects and when arraySizes pass by I stack them as simple integers. Then when it comes time to create the entry I pop while int to get array sizes and then pop 1,2 for the type and ID.

The most complex mechanism I use for attribute migration allows me to nest variable and function calls inside indices of arrays and inside function calls.

The mechanism works as follows:
description for nested variable calls in indices:
    In the semantic analyser, I use the variable indice_lists a a list of lists. At the start of an indice for a variable assign or variable call, a  new list is appended to the main list. everytime a operand/operator/factor is encountered it appends to the top list and if a variable call is encountered and it has indices, the entry is appended to the top as normal, but then a new list is pushed to handle the nested arith expression that could contain more nested variable calls. When an indice finishes, append it to the index section of the last entry of the list below the indice_lists top (should be the pending variable call entry). when the indices finish for a given variable call, check if the variable exists and the correct number of dimensions were specified.

The mechanism to warn about circular class dependancies is one I am quite proud of. It will detect a potential circular dependancy even through nested functions and multiple classes in between. It works as follows:
    - During the first pass, every time I create a class or global function I place it in the classUsageDict{}. And each dict key (which would be the function or class) would reference all the objects/functions that object references.
    - Now in the second pass I have a special recursive function (checkCircularReference()) that for each key and for each respective entry I check in the key fir each entry, if it could somehow make it back to the current root check key. If it does then my program gives a warning that a potential circular dependency could occur and cause an infinite loop.

--- Type Checking ---
My type checking is correct and works but implements the 'sledge hammer' method as my old algorithmic design professor used to say. I know the method in class was supposed to evaluate as a tree in an elegant manner, but unfortunately at the end of the semester with all of my projects and demos witha  job interview process I just thought to myself get it done! make it work asap! My type checking of a complex expression is fullproof for the assignment specs but lacks the ability to be scaled nicely. Once the semester is over I intend to rewrite my entire compiler in C++ and rething this function among a few other components and structures to operate in a more elegant fashion.


--- Errors ---
- Errors are reported at the bottom of the debug output file log files.
- All error locations specified are accurate to the original input test file and not the debug output displayed above the errors
- The production function is also listed at the beginning of the error to help you understand what the parser is expecting.

!- My error recovery technique currently works to re syncronize both the parsing stack and the lookahead scanner to the closest generic/common sync_token expected in the parsing stack e.g. [';', '{', '}']


--- Description of method used to apply any changes to the my grammar. ---
- When I need to make changes to my grammar I have to revert to my version without the upgraded semantic symbols and make changes in KFGedit then place all the semantic symbols back in and make any changes to them if necessary. This method is very crude because then I need to read all the first and follow sets to update them in my specially formatted grammar+ first and follow set file by hand. when my program runs it reads from this specially formatted file and creates all the production objects for me to work with.

--- Grammar Object ---
- The Grammar.py file

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
