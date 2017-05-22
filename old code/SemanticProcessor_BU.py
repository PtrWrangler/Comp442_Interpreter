from Symbol_Table import Symbol_Table, Entry
from Lexer import Token


class SemanticProcessor(object):
    def __init__(self):
        # symbol tables,
        self.level = 0
        self.SymbolTable_stack = []
        # self.SymbolTables = ''
        # hold attrs while processing a table entry using the grammar rules
        self.attr_buffer = []
        # buffers last token
        self.prevToken_buffer = ''
        ''' stores references to class declarations and instantiations for 'second pass' use when checking for:
            undefined class reference and circular class dependancy '''
        self.classUsageDict = {}
        # operator and operand stacks use for complex arithmatic expression evaluation.
        self.operator_stack = []
        self.operand_stack = []

        self.arithExpr_list = []

        # the semantic functions dictionary to use when a semantic symbol is poped
        self.dispatcher = {'CREATE_GLOBAL_TABLE': self.CREATE_GLOBAL_TABLE,
                           'CLASS_ENTRY_TABLE': self.CLASS_ENTRY_TABLE,
                           'END_CLASS': self.END_CLASS,

                           'ENTRY_TYPE': self.ENTRY_TYPE,
                           'ENTRY_NAME': self.ENTRY_NAME,

                           'ADD_DECL_ARRAY': self.ADD_DECL_ARRAY,
                           'VAR_ENTRY': self.VAR_ENTRY,

                           'FUNC_ENTRY_TABLE': self.FUNC_ENTRY_TABLE,
                           'ADD_FUNC_PARAM_ENTRY': self.ADD_FUNC_PARAM_ENTRY,
                           'END_FUNC': self.END_FUNC,

                           'PROGRAM_FUNC_ENTRY_TABLE': self.PROGRAM_FUNC_ENTRY_TABLE,

                           # var assignment checking functions

                           'ENTRY_NEST': self.ENTRY_NEST,
                           'ADD_INDICE_DIM': self.ADD_INDICE_DIM,
                           'CHECK_VAR_EXIST': self.CHECK_VAR_EXIST,

                           'APPEND_OP': self.APPEND_OP,
                           'BEGIN_FUNC_CALL': self.BEGIN_FUNC_CALL,
                           'END_FACTOR_FUNC': self.END_FACTOR_FUNC,
                           'END_FACTOR_VAR': self.END_FACTOR_VAR,

                           # end program function and first pass, begin second pass

                           'END_PROGRAM': self.END_PROGRAM

                           }
        self.error = ""
        self.warnings = ""

    def __str__(self):
        """String representation of the class instance."""

        return 'Semantic Processor'

    def __repr__(self):
        return self.__str__()

    ''''''''''''''''''''''''''''''
    '''   SEMANTIC FUNCTIONS   '''
    ''''''''''''''''''''''''''''''

    def CREATE_GLOBAL_TABLE(self):
        self.SymbolTable_stack.append(Symbol_Table(self.level, 'global'))
        # self.SymbolTables = Symbol_Table(self.level, 'global')

    ##################################################################
    #                     CLASS SEMANTIC ACTIONS                     #
    ##################################################################
    def CLASS_ENTRY_TABLE(self):
        print "create_classEntryAndTable."
        # ensure class name does not already exist in Global Table
        class_entry = Entry(self.level, self.prevToken_buffer.value, 'class', '')
        if self.SymbolTable_stack[0].search(class_entry) is None:

            # log class name in classDict if not there
            if class_entry.name not in self.classUsageDict:
                self.classUsageDict[class_entry.name] = []

            # create a table entry and link it to the new class table
            self.level += 1
            class_entry.link = Symbol_Table(self.level, class_entry.name)

            # append the new entry to the global table and put the reference to the class table on top the stack
            if self.SymbolTable_stack:
                self.SymbolTable_stack[-1].addEntry(class_entry)
            self.SymbolTable_stack.append(class_entry.link)

        else:
            # error this class name alreay exists in global table
            print "Attempting new class entry/table but name " + self.prevToken_buffer.value + " already exists in global table"
            self.error += "\nError: Duplicate class declaration: " + str(self.prevToken_buffer)
            print self.error

    def END_CLASS(self):
        print 'ending class.'
        if self.SymbolTable_stack:
            self.SymbolTable_stack.pop()
        self.level -= 1

    def ENTRY_TYPE(self):
        print "buffering entryType"
        self.attr_buffer = []
        self.attr_buffer.append(self.prevToken_buffer)

    def ENTRY_NAME(self):
        print "buffering entryName"
        self.attr_buffer.append(self.prevToken_buffer)

    def ADD_DECL_ARRAY(self):
        print 'adding an array decl dimension size'
        self.attr_buffer.append(int(self.prevToken_buffer.value))

    def FUNC_ENTRY_TABLE(self):
        print "create_funcEntryAndTable."
        # ensure function name does not already exist in current scope
        if len(self.attr_buffer) > 1:
            func_name = self.attr_buffer.pop()
            func_type = self.attr_buffer.pop()

        # create a new global/local table entry and link it to the new class table
        entry = Entry(self.level, func_name.value, 'function', func_type.value)
        self.level += 1
        entry.link = Symbol_Table(self.level, entry.name)

        if self.SymbolTable_stack[-1].search(entry) is None:

            # check if in class or global table
            if len(self.SymbolTable_stack) <= 1:
                if entry.name not in self.classUsageDict:
                    self.classUsageDict[entry.name] = []

            # append the new entry to the global/class table and put the reference to the class table on top the stack
            if self.SymbolTable_stack:
                self.SymbolTable_stack[-1].addEntry(entry)
            self.SymbolTable_stack.append(entry.link)
        else:
            # error this function name alreay exists in scope
            print "Attempting new function but name " + func_name.value + " already exists in scope"
            self.error += "\nError: Duplicate function declaration: " + str(func_name)
            print self.error

    def ADD_FUNC_PARAM_ENTRY(self):
        print 'adding a function parameter entry.'

        entry = Entry(self.level, '', 'parameter', '')
        while isinstance(self.attr_buffer[-1], int):
            entry.arraySize.insert(0, self.attr_buffer.pop())
        if len(self.attr_buffer) > 1:
            nameToken = self.attr_buffer.pop()
            entry.name = nameToken.value
            entry.type = self.attr_buffer.pop().value

        # if variable already in scope give warning
        if self.check_var_in_scope(entry):
            self.warnings += "\nWarning: Parameter name already exists in scope: " + str(nameToken)

        if self.SymbolTable_stack:
            self.SymbolTable_stack[-1].addEntry(entry)

        # modify the type of the function entry two layers back
        if len(self.SymbolTable_stack) > 1:
            self.SymbolTable_stack[-2].append_param_to_func_entry_type(self.SymbolTable_stack[-1], entry)

    def END_FUNC(self):
        print 'ending class function'
        if self.SymbolTable_stack:
            self.SymbolTable_stack.pop()
        self.level -= 1

    def VAR_ENTRY(self):
        print "creating create_varEntry."
        # create a new class table entry for a variable
        entry = Entry(self.level, '', 'variable', '')
        while isinstance(self.attr_buffer[-1], int):
            entry.arraySize.insert(0, self.attr_buffer.pop())
        if len(self.attr_buffer) > 1:
            nameToken = self.attr_buffer.pop()
            entry.name = nameToken.value
            typeToken = self.attr_buffer.pop()
            entry.type = typeToken.value

        # if variable already in scope give warning
        if self.check_var_in_scope(entry):
            self.warnings += "\nWarning: Variable name already exists in scope: " + str(nameToken)

        # if type is a UD_Type, put in dict for 'second pass' circular class dependency checking
        if entry.type != 'int' and entry.type != 'float' and len(self.SymbolTable_stack) > 1 and self.SymbolTable_stack[1].name != 'program':
            if self.SymbolTable_stack[1].name in self.classUsageDict:
                if typeToken not in self.classUsageDict[self.SymbolTable_stack[1].name]:
                    self.classUsageDict[self.SymbolTable_stack[1].name].append(typeToken)
            else:
                self.classUsageDict[self.SymbolTable_stack[1].name] = []

        # append the new entry to the class table
        if self.SymbolTable_stack:
            self.SymbolTable_stack[-1].addEntry(entry)

    def PROGRAM_FUNC_ENTRY_TABLE(self):
        print 'adding the program function entry and symbol_table.'
        # create a new global table entry and link it to the new main program function table
        entry = Entry(self.level, 'program', 'function', '')
        self.level += 1
        entry.link = Symbol_Table(self.level, entry.name)

        # append the new entry to the global table and put the reference to the program table on top the stack
        if self.SymbolTable_stack:
            self.SymbolTable_stack[-1].addEntry(entry)
        self.SymbolTable_stack.append(entry.link)

    '''''''''''''''''''''' VAR ASSIGNMENT TYPING '''''''''''''''''''''''

    def APPEND_OP(self):
        print 'Appending operator/operand'
        # self.arithExpr_list.append(self.attr_buffer)

    def ADD_INDICE_DIM(self):
        print 'add indice dimension (arithExpr)'
        # self.attr_buffer.append(self.arithExpr_list)
        # self.arithExpr_list = []

    def ENTRY_NEST(self):
        print "specifying object nested variable"
        # entry = Entry(self.level, '', 'variable', '')
        # while isinstance(self.attr_buffer[-1], int):
        #     entry.arraySize.insert(0, self.attr_buffer.pop())
        # if len(self.attr_buffer) > 1:
        #     nameToken = self.attr_buffer.pop()
        #     entry.name = nameToken.value
        #     entry.type = self.attr_buffer.pop().value

    def CHECK_VAR_EXIST(self):
        print "Checking if Variable has been declared for use"
        print self.attr_buffer

        if len(self.attr_buffer) > 0:
            nameToken = self.attr_buffer.pop()
            temp_entry = Entry(self.level, nameToken.value, 'variable', '')
            if not self.check_var_in_scope(temp_entry):
                self.error += "\nError: Variable or Parameter has not been declared: " + str(nameToken)
        # print "Checking if Variable has been declared for use"
        # print self.attr_buffer
        #
        # entry = Entry(self.level, '', 'assignment', '')
        # # get all arithExpr indices specified and save them in the assignment entry
        # while isinstance(self.attr_buffer[-1], list):
        #     entry.indice.append(self.attr_buffer.pop())
        # if len(self.attr_buffer) > 0:
        #     nameToken = self.attr_buffer.pop()
        #     entry.name = nameToken.value
        #
        # self.check_var_and_indice_in_scope(entry)


    def BEGIN_FUNC_CALL(self):
        print 'Beginning factor func call.'
        # self.operator_stack = []
        # self.operand_stack = []

    def END_FACTOR_FUNC(self):
        print 'Ending factor func call.'
        # self.operator_stack.append(self.prevToken_buffer)

    def END_FACTOR_VAR(self):
        print 'Ending factor variable.'
        # self.operand_stack.append(self.prevToken_buffer)

    '''''''''''''''''''''' END PROGRAM FUNCTION AND FIRST PASS, BEGIN SECOND PASS '''''''''''''''''''''''

    def END_PROGRAM(self):
        print "End of main program function (and whole program)"
        if self.SymbolTable_stack:
            self.SymbolTable_stack.pop()
        self.level -= 1

        for i in self.classUsageDict:
            print i, self.classUsageDict[i]

        # Start 'second pass' to check for:
        # UD_Type correctness
        for key in self.classUsageDict:
            for val in self.classUsageDict[key]:
                if val.value not in self.classUsageDict:
                    print 'Error: Class type does not exist'
                    self.error += "\nError: Class type \'" + str(val) + "\' does not exist."
                    break

        # circular class function dependency
        if self.error == "":
            warning = False
            for key in self.classUsageDict:
                #key = Token()
                if key in self.classUsageDict[key]:
                    print 'Warning: direct circular reference in ' + str(key)
                    self.warnings += "\nWarning: Possible direct circular reference through " + str(key) + " and " + str(val)
                else:
                    for val in self.classUsageDict[key]:
                        if self.checkCircularReference(key, key, val):
                            warning = True
                            break
                if warning:
                    break

    '''''''''''''''''''''' Tools '''''''''''''''''''''''

    def check_var_in_scope(self, entry):
        print self.SymbolTable_stack

        for table in reversed(self.SymbolTable_stack):
            foundEntry = table.search(entry)
            if isinstance(foundEntry, Entry):
                return True
        return False

    def check_var_and_indice_in_scope(self, entry):
        print self.SymbolTable_stack

        for table in reversed(self.SymbolTable_stack):
            foundEntry = table.search(entry)
            if isinstance(foundEntry, Entry):
                found = True
                if len(foundEntry.indice) != len(entry.indice):
                    self.error += "\nError: Incorrect array dimensions for index of: " + entry.name # str(nameToken)
        if not found:
            self.error += "\nError: Variable or Parameter has not been declared: " + entry.name # str(nameToken)

    def appendToClassUsageDict(self, classOrGlobFuncName):
        print 'in appendToClassUsageDict()'

    def checkCircularReference(self, originalKey, key, val):
        print 'in check circular reference'

        end = False
        if originalKey in self.classUsageDict[val.value]:
            print 'Warning: Possible circular reference through ' + str(originalKey) + ' and ' + str(val)
            self.warnings += "\nWarning: Possible circular reference through " + str(originalKey) + " and " + str(val)
            end = True
        else:
            for nextVal in self.classUsageDict[val.value]:
                if self.checkCircularReference(originalKey, val, nextVal):
                    end = True
                    break
        return end

