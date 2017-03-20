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

        return '\n' + tabs + 'Symbol_Table(lvl: {lvl}, name:{name}, entries:{entries})'.format(
            lvl=self.level,
            name=self.name,
            entries=self.entries
        )

    def __repr__(self):
        return self.name

    def addEntry(self, entry):
        print "adding entry to: " + self.name + " table."
        self.entries.append(entry)

    def create(self, table_name):
        print "creating table"

    def search(self, table_name, i, ptr, found):
        print "searching table"

    def insert(self, table_name, i, ptr):
        print "inserting entry"

    def delete(self, table_name):
        print "deleting table"

    def Print(self, table_name):
        print "printing table"


class Entry(object):
    def __init__(self, level, name, kind, typ):

        self.name = name
        self.kind = kind
        self.type = typ
        self.link = None

        self.level = level

    def __str__(self):
        """String representation of the class instance."""

        tabs = ''
        for j in range(self.level):
            tabs += '    '

        return '\n' + tabs + 'Entry( lvl:{lvl}, {name}, {kind}, {type}, link: {link} )'.format(
            lvl=self.level,
            name=self.name,
            kind=repr(self.kind),
            type=repr(self.type),
            link=str(self.link)
        )

    def __repr__(self):
        return self.__str__()

