import re


class Symbol_Table(object):
    def __init__(self, level, name):

        self.name = name
        self.entries = []

        self.level = level

    def __str__(self):
        """String representation of the class instance."""

        tabs = ''
        for j in range(self.level):
            tabs += '    '

        return '\n' + tabs + 'Sym_Tbl(name:{name}, entries:{entries})'.format(
            # lvl=self.level,
            name=self.name,
            entries=self.entries
        )

    def __repr__(self):
        return self.name

    def addEntry(self, entry):
        print "adding entry to: " + self.name + " table."
        self.entries.append(entry)

    def append_param_to_func_entry_type(self, func_name, param_entry):
        print 'adding parameter to function\'s entry type'
        function_entry = self.search(func_name)

        if function_entry is not None:

            arrSize = ''
            if param_entry.arraySize:
                for i in param_entry.arraySize:
                    arrSize += '[' + str(i) + ']'

            if ':' in function_entry.type:
                function_entry.type += ', ' + param_entry.name + arrSize
            else:
                function_entry.type += ' : ' + param_entry.name + arrSize

    def search(self, entry_name):
        print "searching " + self.name + " table"
        for e in self.entries:
            if e.name == entry_name:
                return e

        print 'entry not found'
        return None

    def delete(self, entry_name):
        print "deleting table"
        entry = self.search(entry_name)
        if entry:
            del self.entries

    def Print(self, table_name):
        print "printing table"


class Entry(object):
    def __init__(self, level, name, kind, typ):

        self.name = name
        self.kind = kind
        self.type = typ
        self.arraySize = []
        self.link = None

        # to be used in code generation
        self.memory_location = 0
        self.assembly_code_alias = ''

        self.level = level

    def __str__(self):
        """String representation of the class instance."""

        tabs = ''
        for j in range(self.level):
            tabs += '    '

        arrSize = ''
        if self.arraySize:
            for i in self.arraySize:
                arrSize += '[' + str(i) + ']'

        return '\n' + tabs + 'Entry  ({name}, {kind}, {type}{arraySize}, link: {link} )'.format(
            # lvl=self.level,
            name=self.name,
            kind=repr(self.kind),
            type=repr(self.type),
            arraySize=arrSize,
            link=str(self.link)
        )

    def __repr__(self):
        return self.__str__()

