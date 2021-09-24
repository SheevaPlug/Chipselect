#!/usr/bin/env python
import os
import sys
import traceback
from pathlib import Path
from argparse import ArgumentParser
from collections import OrderedDict

import xmltodict
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk as esbulk


counter = 0

def clean_dict(d):
    global counter
    '''recursively clean the '@' prefixes in attribute names'''
    rv = {}
    try:
        d.keys()
        for key in d.keys():
            if key.startswith('@'):
                if type(d[key]) is dict or type(d[key]) is OrderedDict:
                    rv[key[1:]] = clean_dict(d[key])
                elif type(d[key]) is list:
                    nv = []
                    for item in d[key]:
                        nv.append(clean_dict(item))
                    rv[key[1:]] = nv
                else:
                    rv[key[1:]] = d[key]
            else:
                if type(d[key]) is dict or type(d[key]) is OrderedDict:
                    rv[key] = clean_dict(d[key])
                elif type(d[key]) is list:
                    nv = []
                    for item in d[key]:
                        nv.append(clean_dict(item))
                    rv[key] = nv
                else:
                    rv[key] = d[key]
    except:
        print(d)
        print(traceback.print_exc())
        counter += 1
    return rv


class Walker:
    def __init__(self, args):
        self.args = args
        self.es = Elasticsearch()
        self.filenames = set()
        self._walk()
        self._read_files()

    def _walk(self):
        for directory in self.args.input_dirs:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    fullname = Path(dirpath, filename)
                    if str(fullname).lower().endswith('.svd'):
                        self.filenames.add(fullname)

    def _read_files(self):
        actions = []
        for filename in self.filenames:
            with open(filename) as ifh:
                #df = pd.read_xml(ifh)
                #df.dropna()
                #print(df)
                #device = clean_dict(xmltodict.parse(ifh.read(), xml_attribs=True))
                device = xmltodict.parse(ifh.read(), xml_attribs=True)
                #print(device)
                device = device.get('device', None)
                if device:
                    actions.append({
                        '_op_type': 'index',
                        '_index': 'mcs',
                        '_source': device})
                    if len(actions) % 100:
                        esbulk(self.es, actions)
                        actions = []
                


if __name__ == '__main__':
    parser = ArgumentParser(description='find and import svd files')
    parser.add_argument('input_dirs', nargs='+', help='where the files are')
    args = parser.parse_args()

    walker = Walker(args)

    print('counter:', counter)
