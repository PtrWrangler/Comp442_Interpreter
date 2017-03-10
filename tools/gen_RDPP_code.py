import string
from Lexer import IDENTIFIER
from Lexer import FLOAT
from Lexer import INTEGER

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def main():
    starter_code = open('starter_code.py', 'r')

    with open('../newDriver.py', 'w+') as o:
        for l in starter_code.readlines():
            o.write(l)

        with open('../Grammar Notes/FIRST and FOLLOW sets.txt', 'r') as f:

            function = ''
            RHSs = []
            current_func = ''
            count = 0
            for l in f.readlines():
                if '->' in l:
                    function = ''
                    count = 1
                    current_func = l.partition(' ')[0]
                    RHS = l.split('-> ')[-1].split(' | EPSILON')[0]
                    RHS = RHS.replace(' \r\n', '')
                    RHSs = RHS.split(' ')
                    RHSs[-1] = RHSs[-1].replace('\r\n', '')

                    print RHS
                    print RHSs

                    function += '    def ' + current_func + '(self):\n'
                    function += '        print \'Syntactical_Parser: in ' + current_func + '\'\n'

                    o.write(function)
                    print function

                if 'first: ' in l:
                    first_body = ''
                    first_body += '        if self.lookahead.value in ff_sets.' + current_func + '_FIRST' + str(count) + ' or '
                    first_body += 'self.lookahead.type in ff_sets.' + current_func + '_FIRST' + str(count) + ':\n'

                    first_body += '            while self.lookahead.type != \'$\':\n'
                    first_body += '                if '

                    if RHS.count('|') > 0:
                        current_rhs = RHS.split('|')[count].split(' ')
                        print current_rhs

                    '''for rhs in RHSs[:-1]:
                        if rhs != '|':
                            first_body += 'self.' + rhs + '() and '''

                    first_body += 'self.' + RHSs[-1] + ':\n\n'

                    first_body += '                print \'' + current_func + ' -> \'\n'
                    #for rhs in RHSs


                    o.write(first_body)
                    print first_body

                if 'follow: ' in l:

                    ff = current_func + '_FOLLOW = ' + l
                    o.write('#' + ff)
                    print ff


if __name__ == '__main__':
        main()
