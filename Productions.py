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

        rule_id = 0
        follow_set = False
        prod = Production(0, "null", "null")

        with open(grammar_specs_file, 'r') as f:
            for l in f.readlines():
                if '->' in l:

                    prod_str = l.replace(' \n', '').replace('\n', '')
                    prod_str = re.sub(' {2,}', ' ', prod_str)

                    name = prod_str.split('->')[0].replace(' ', '')
                    self.productions[rule_id] = Production(rule_id, name, prod_str)
                    rule_id += 1

                    if 'EPSILON' in l:
                        follow_set = True

                elif follow_set is False:
                    if 'EPSILON' in l:
                        follow_set = True

                    self.productions[rule_id-1].first = get_list_from_line(l)

                elif follow_set is True:
                    self.productions[rule_id-1].follow = get_list_from_line(l)
                    follow_set = False


class Production(object):
    def __init__(self, r_id, name, production):
        # unique rule identifier
        self.r_id = r_id

        self.name = name

        self.str_production = production
        self.first = []
        self.follow = []

    def __str__(self):
        """String representation of the class instance."""

        return 'Production({id}, {prod}, \n\tfirst={first}\n\tfollow={follow}\n'.format(
            id=self.r_id,
            prod=repr(self.str_production),
            first=self.first,
            follow=self.follow
        )

    def __repr__(self):
        return self.str_production
