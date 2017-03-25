from Symbol_Table import Symbol_Table, Entry
import copy


class SemanticProcessor(object):
    def __init__(self):
        # symbol tables,
        self.level = 0
        self.SymbolTable_stack = []
        # hold attrs while processing a table entry using the grammar rules
        self.prevToken_buffer = ''
        self.fParam_buffer = []
        self.entry_buffer = Entry(self.level, '', '', '')
        # the semantic functions dictionary to use when a semantic symbol is poped
        self.dispatcher = {'CREATE_GLOBAL_TABLE': self.CREATE_GLOBAL_TABLE,
                           'CLASS_ENTRY_TABLE': self.CLASS_ENTRY_TABLE,
                           'END_CLASS': self.END_CLASS,

                           'ENTRY_TYPE': self.ENTRY_TYPE,
                           'ENTRY_NAME': self.ENTRY_NAME,
                           'ADD_DECL_ARRAY_DIM': self.ADD_DECL_ARRAY_DIM,

                           'CLASS_VAR_ENTRY': self.CLASS_VAR_ENTRY,
                           'FUNC_ENTRY_TABLE': self.FUNC_ENTRY_TABLE,
                           # 'PARAM_TYPE': self.PARAM_TYPE,
                           # 'PARAM_NAME': self.PARAM_NAME,
                           # 'PARAM_NAME': self.PARAM_NAME,
                           'ADD_FUNC_PARAM_ENTRY': self.ADD_FUNC_PARAM_ENTRY,
                           'END_CLASS_FUNC': self.END_CLASS_FUNC,

                           'PROGRAM_FUNC_ENTRY_TABLE': self.PROGRAM_FUNC_ENTRY_TABLE

                           }

    def __str__(self):
        """String representation of the class instance."""

        return 'test'

    def __repr__(self):
        return self.__str__()

    def clearEntryBuffer(self):
        self.entry_buffer.name = ''
        self.entry_buffer.type = ''
        self.entry_buffer.kind = ''
        self.entry_buffer.arraySize = []
        self.entry_buffer.link = None

    ''''''''''''''''''''''''''''''
    '''   SEMANTIC FUNCTIONS   '''
    ''''''''''''''''''''''''''''''

    def CREATE_GLOBAL_TABLE(self):
        self.SymbolTable_stack.append(Symbol_Table(self.level, 'global'))

    ##################################################################
    #                     CLASS SEMANTIC ACTIONS                     #
    ##################################################################
    def CLASS_ENTRY_TABLE(self):
        print "create_classEntryAndTable."
        # create a table entry and link it to the new class table
        class_entry = Entry(self.level, self.prevToken_buffer, 'class', '')
        self.level += 1
        class_entry.link = Symbol_Table(self.level, class_entry.name)

        # append the new entry to the global table and put the reference to the class table on top the stack
        self.SymbolTable_stack[-1].addEntry(class_entry)
        self.SymbolTable_stack.append(class_entry.link)

    def END_CLASS(self):
        print 'ending class.'
        self.SymbolTable_stack.pop()
        self.level -= 1

    def ENTRY_TYPE(self):
        print "buffering entryType"
        self.SymbolTable_stack.append(self.prevToken_buffer)
        #self.entry_buffer.type = self.prevToken_buffer

    def ENTRY_NAME(self):
        print "buffering entryName"
        self.SymbolTable_stack.append(self.prevToken_buffer)
        #self.entry_buffer.name = self.prevToken_buffer

    def FUNC_ENTRY_TABLE(self):
        print "create_funcEntryAndTable."
        # create a new global/local table entry and link it to the new class table
        #entry = Entry(self.level, self.SymbolTable_stack.pop(), 'function', self.SymbolTable_stack.pop())
        self.entry_buffer.level = self.level
        self.entry_buffer.kind = 'function'
        self.level += 1
        self.entry_buffer.link = Symbol_Table(self.level, self.entry_buffer.name)

        # append the new entry to the global table and put the reference to the class table on top the stack
        entry = copy.deepcopy(self.entry_buffer)
        self.SymbolTable_stack[-1].entries.append(entry)
        self.SymbolTable_stack.append(entry.link)

        self.clearEntryBuffer()

    def END_CLASS_FUNC(self):
        print 'ending class function'
        self.SymbolTable_stack.pop()
        self.level -= 1

    def ADD_DECL_ARRAY_DIM(self):
        print 'adding an array decl dimension size'
        self.entry_buffer.arraySize.append(int(self.prevToken_buffer))

    def ADD_FUNC_PARAM_ENTRY(self):
        print 'adding a function parameter entry.'

    def CLASS_VAR_ENTRY(self):
        print "creating create_varEntry."
        # create a new class table entry and link it to the new class table
        self.entry_buffer.level = self.level
        self.entry_buffer.kind = 'variable'

        # append the new entry to the global table and put the reference to the class table on top the stack
        entry = copy.deepcopy(self.entry_buffer)
        self.SymbolTable_stack[-1].entries.append(entry)

        self.clearEntryBuffer()

    def PROGRAM_FUNC_ENTRY_TABLE(self):
        print 'adding the program function entry and symbol_table.'
        # create a new global/local table entry and link it to the new class table
        self.entry_buffer.level = self.level
        self.entry_buffer.name = 'program'
        self.entry_buffer.kind = 'function'
        self.level += 1
        self.entry_buffer.link = Symbol_Table(self.level, self.entry_buffer.name)

        # append the new entry to the global table and put the reference to the class table on top the stack
        entry = copy.deepcopy(self.entry_buffer)
        self.SymbolTable_stack[-1].entries.append(entry)
        self.SymbolTable_stack.append(entry.link)

        self.clearEntryBuffer()

