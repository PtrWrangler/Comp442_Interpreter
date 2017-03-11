

class Production(object):
    def __init__(self, r_id, name, production):
        # unique rule identifier
        self.r_id = id

        self.name = name

        self.str_production = production
        self.rhs = []
        self.set = []

    def __str__(self):
        """String representation of the class instance."""

        return 'Token({type}, {value}, Line:Pos=({line}, {pos}))'.format(
            type=self.type,
            value=repr(self.value),
            line=self.line,
            pos=self.pos
        )

    def __repr__(self):
        return self.__str__()