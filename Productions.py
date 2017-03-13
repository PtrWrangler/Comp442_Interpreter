import re


def rreplace(s, old, new, num_occurrence):
    li = s.rsplit(old, num_occurrence)
    return new.join(li)


def get_list_from_line(l):
    s = l.replace('[', '', 1)
    s = s.replace('\n', '')
    s = rreplace(s, ']', '', 1)
    return s.split(', ')


class Grammar(object):
    def __init__(self):

        self.productions = {}

        grammar_specs_file = "Grammar Notes/PPT_Grammar.txt"
        # initialize list of productions from input file
        self.parse_grammar_file(grammar_specs_file)

    def __str__(self):
        """String representation of the class instance."""

        s = "\n __ALL PRODUCTIONS__\n"
        for r in self.productions:
            s += self.productions[r].__str__()
        return s
        # return 'Token({type}, {value}, Line:Pos=({line}, {pos}))'.format(
        #     type=self.type,
        #     value=repr(self.value),
        #     line=self.line,
        #     pos=self.pos
        # )

    def __repr__(self):
        return self.__str__()

    def parse_grammar_file(self, grammar_specs_file):

        production_id = 0
        prev_name = ""
        follow_set = False

        with open(grammar_specs_file, 'r') as f:
            for l in f.readlines():
                if '->' in l:

                    # remove trailing \n, multi spaces. extract name, RHS terminals/non-terminals
                    prod_str = l.replace(' \n', '').replace('\n', '')
                    prod_str = re.sub(' {2,}', ' ', prod_str)
                    name = prod_str.split('->')[0].replace(' ', '')

                    rhs_str = prod_str.split('-> ')[1]
                    rhs = rhs_str.split(' ')
                    rhs_str = " | " + rhs_str

                    if name != prev_name:
                        prev_name = name
                        self.productions[name] = Production(production_id, name, prod_str)
                        production_id += 1
                        rhs_str = ""

                    self.productions[name].add_RHS(Right_hand_side(production_id, name, rhs), rhs_str)

                    if 'EPSILON' in l:
                        follow_set = True

                elif follow_set is False:
                    if 'EPSILON' in l:
                        follow_set = True

                    self.productions[name].RHSs[-1].first = get_list_from_line(l)

                elif follow_set is True:
                    self.productions[name].RHSs[-1].follow = get_list_from_line(l)
                    follow_set = False


class Production(object):
    def __init__(self, p_id, name, production_str):
        # unique rule identifier
        self.p_id = p_id

        self.name = name
        self.str_production = production_str

        self.RHSs = []

    def __str__(self):
        """String representation of the class instance."""

        return 'Production({id}, {prod}, {RHS}\n'.format(
            id=self.p_id,
            prod=repr(self.str_production),
            RHS=repr(self.RHSs)
        )

    def __repr__(self):
        return self.str_production

    def add_RHS(self, rhs, rhs_str):
        self.RHSs.append(rhs)
        self.str_production += rhs_str


class Right_hand_side(object):
    def __init__(self, p_id, name, rhs):

        self.p_id = p_id
        self.name = name

        self.RHS = rhs
        self.first = []
        self.follow = []
        # self.rhs_str = ' '.join(self.RHS)

    def __str__(self):
        """String representation of the class instance."""
        return ' '.join(self.RHS)

    def __repr__(self):
        return ' '.join(self.RHS)
        # return '\n\tRHS({RHS}\n\t\tfirst={first}\n\t\tfollow={follow}\t'.format(
        #     RHS=self.RHS,
        #     first=self.first,
        #     follow=self.follow
        # )

    def inverse_RHS_multiple_push(self):
        rev_rhs = []
        for i in reversed(self.RHS):
            rev_rhs.append(i)
        return rev_rhs
