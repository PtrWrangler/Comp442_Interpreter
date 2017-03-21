

class SemanticProcessor(object):
    def __init__(self):



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

