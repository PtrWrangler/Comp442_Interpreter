
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def main():
    with open('../ff_sets.py', 'w+') as o:
        with open('../Grammar Notes/FIRST and FOLLOW sets.txt', 'r') as f:

            current_func = ''
            count = 0
            for l in f.readlines():
                if '->' in l:
                    count = 1
                    current_func = l.partition(' ')[0]

                if 'first: ' in l:
                    l = l.replace('{', '[\'', 1)
                    l = l.replace(', ', '\', \'')
                    l = rreplace(l, '}', '\']', 1)
                    l = l.replace('\tfirst: ', '')
                    ff = current_func + '_FIRST' + str(count) + ' = ' + l
                    count += 1
                    o.write(ff)
                    print ff

                if 'follow: ' in l:
                    l = l.replace('{', '[\'', 1)
                    l = l.replace(', ', '\', \'')
                    l = rreplace(l, '}', '\']', 1)
                    l = l.replace('\tfollow: ', '')
                    ff = current_func + '_FOLLOW = ' + l
                    o.write(ff)
                    print ff


if __name__ == '__main__':
        main()
