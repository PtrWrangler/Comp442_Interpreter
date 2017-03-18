import re


class Symbol_Table(object):
    def __init__(self, name):

        self.name = name
        self.entries = []

    def __str__(self):
        """String representation of the class instance."""

        return 'Symbol_Table({name})'.format(
            name=self.name
        )

    def __repr__(self):
        return self.__str__()

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
    def __init__(self, name, kind, type):

        self.name = name
        self.kind = kind
        self.type = type
        self.link

    def __str__(self):
        """String representation of the class instance."""

        return 'Production({name}, {kind}, {type}\n'.format(
            name=self.name,
            kind=repr(self.kind),
            type=repr(self.type)
        )

    def __repr__(self):
        return self.__str__()

