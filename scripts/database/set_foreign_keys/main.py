#!/usr/bin/env python
FILENAME = 'fk1.txt'

from psycopg2 import connect


def split_stripped(line, delimiter='='):
    return list(map(lambda s: s.strip(), line.split(delimiter)))

class ForeignKey:
    def __init__(self, line):
        self.line = line
        t, f = split_stripped(self.line)
        self.child_table, self.child_column = split_stripped(t, '.')
        self.parent_table, self.parent_column = split_stripped(f, '.')
        self.fk_name = 'fk_{}_{}'.format(self.parent_table, self.parent_column)

    def sql(self):
        return '''ALTER TABLE {x.child_table} ADD CONSTRAINT {x.fk_name} FOREIGN KEY ({x.child_column}) REFERENCES {x.parent_table} ({x.parent_column});'''.format(x=self)


if __name__ == '__main__':
    with open(FILENAME, 'r') as ifh: fks = [ForeignKey(line.strip()) for line in ifh]
    conn = connect()
    for fk in fks:
        try:
            print(fk.sql())
            curs = conn.cursor()
            curs.execute(fk.sql())
            curs.close()
        except Exception as e:
            print('ERROR:', str(e))
            pass
    conn.commit()
    conn.close()
