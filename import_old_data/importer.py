#!/usr/bin/env python
from argparse import ArgumentParser

import psycopg2 as PG
from psycopg2.extras import DictCursor
from elasticsearch import Elasticsearch as ES


def clean_empty_fields(result):
    '''removes keys from a dict if their value is in ["None", None]'''
    return {key: value for key, value in result.items() if value and value is not None}


def clean_empty_results(results):
    '''cleans lists of database return value dicts from keys in ["None", None]'''
    return [clean_empty_fields(dict(result)) for result in results]


class Controllers:
    '''ALL controllers'''
    def __init__(self, conn, limit):
        self.conn = conn
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute('''SELECT * FROM microcontroller m LIMIT %s''', [limit])
            self.controllers = [Controller(self.conn, uc) for uc in curs.fetchall()]

class Controller:
    '''ONE controller'''
    def __init__(self, conn, controller):
        self.conn = conn
        self.controller = clean_empty_fields(dict(controller))
        self._init_architecture()

    def _init_architecture(self):
        '''get architecture data and append to myself'''
        with conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute('''SELECT pa.* FROM pl_architecture pl LEFT JOIN p_architecture pa ON pl.arch_id = pa.id WHERE pl.dev_id = %s''', [self.controller.get('id')])
            clean = clean_empty_results(curs.fetchall())
            if clean: self.controller['architecture'] = clean

    def __str__(self):
        '''lean output if converted to str()'''
        return str(self.controller)


if __name__ == '__main__':
    parser = ArgumentParser(description='import data from PostgreSQL into Elasticsearch')
    parser.add_argument('dbname', default='luke', nargs='?')
    parser.add_argument('dbuser', default='luke', nargs='?')
    parser.add_argument('dbpass')
    parser.add_argument('--count', '-c', default=50, help='how many to get')
    args = parser.parse_args()

    with PG.connect(dbname=args.dbname, user=args.dbuser, password=args.dbpass) as conn: 
        for controller in Controllers(conn, args.count).controllers:
            print(controller)
