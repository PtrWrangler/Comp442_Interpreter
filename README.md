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

from your terminal execute the command in the unpacked root project folder
    python driver.py
If you want to change the input testfile (source program),
    open driver.py with your any text editor and specify the testFile name and dir at the top
sample testfiles are in /testing and all outputs and errorlogs are sent to /output


----------------------------------------------------------------------------

--- Important Notes ---
- I have now upgraded to a Table-Driven Predictive Parser (RDPP)

PLEASE UPDATE INFORMATION BELOW:

- All ambiguities were removed without taking away from the expressiveness of the langauge.
- The grammar has been optimized to an LL(1) grammar

- List of changes and notes about the grammar can be found in
    'Grammar Notes/442 A2 grammar change notes.txt'

- My First and Follow sets can be found in
    'Grammar Notes/FIRST and FOLLOW sets.txt'
    - Note: you can also see them in python list format by checking the 'ff_sets.py' file

- My Full updated grammar can be found in
    'Grammar Notes/Grammar.txt'

- outputs are sent to the outputs folder
    NOTE: the spacing of the outputted program is not finished yet so that is why everything looks squished together... that will be fixed in A3.

--- Description of method used to apply changes to the original grammar. ---
- The method I used to apply changes to the original grammar was at first to follow it by eye and use KFGedit. Then once I moved far enough along I began to implement the RDPP code. As I moved forward using the debugger allowed me to discover more ambiguities LL1 condition violations and simply better understand the grammar rules.


--- Description/rationale of the overall structure of the solution ---
- The Parser class implements recursive descent predictive parsing and calls the Lexer for next tokens. Since the RDPP method requires having a ton of functions for each production I created some tools to help me generate them and/or edit them. they are in the 'tools/' folder. Also, there is a tool to help me generate my first and follow sets when I change my grammar.


--- Errors ---
Errors are reported in individual log files.

An error occurs when a productions expected RHS fails.
** Tokens are continuously skipped until the correct expected token is scanned.

Line numbers and cursor positions of all errors are reported.
    * cursor position is at the end of the lexeme match

The production function is also listed at the beginning of the error to help you understand what the parser is expecting.

Looking at the top most error in the error output file will help you the most by telling you where the first problem occured in the likely long cascade of errors afterwards.


--- Tools and Libraries used and Bibliography ---
- KFGedit was a great tool that I used to help me fix the grammar.
    It allowed me to understand what the first and follow sets really meant and understand how they relate to making a grammar LL(1).
- Just using my scripts to help quickly modify my code when I
    modified my grammar.

- A lot of stack overflow...
- the slides
