#!/usr/bin/env python
import sys
import json
from argparse import ArgumentParser

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan as esscan


if __name__ == '__main__':
    parser = ArgumentParser(description='backup elasticsearch instance')
    parser.add_argument('outfile', nargs='?', help='outfile')
    args = parser.parse_args()

    outfile = sys.stdout
    if args.outfile: outfile = open(args.outfile, 'w')

    es = Elasticsearch()
    devices = esscan(es, {})
    outfile.write(json.dumps(list(devices)))
    
    if args.outfile: outfile.close()
