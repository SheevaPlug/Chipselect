#!/usr/bin/env python
import json
from argparse import ArgumentParser

import numpy as np
import pandas as pd
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk as osbulk

OPENSEARCH_PARAMS = {
    'hosts': [{'host': 'localhost', 'port': 9200}], 
    'http_auth': ('admin', 'admin'),
    'use_ssl': True,
    'verify_certs': False,
    'ssl_show_warn': False,
}


def clean_strings(s):
    s = s.str.strip()
    s = s.replace('None', np.nan)
    #s = s.replace('', lambda x: x if len(x) > 0 else np.nan)
    return s

def clean_dict(d):
    return {k: v for k, v in d.items() if v and v is not np.nan} # and v != 'No'}

def set_vendor(d):
    d.update({'vendor': 'Microchip'})
    return d


if __name__ == '__main__':
    parser = ArgumentParser(description='import data from microcontroller_and_processors-2020-08-14.xlsx')
    parser.add_argument('infile', default='microcontroller_and_processors-2020-08-14.xlsx', help='input file')
    parser.add_argument('--tryout', '-t', action='store_true', help='output data instead of writing')
    args = parser.parse_args()

    
    df = pd.read_excel(args.infile)
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(clean_strings)
    df = df.T
    data = [clean_dict(df[d].to_dict()) for d in df]
    if args.tryout:
        from pprint import pprint; pprint(data)
    else:
        ops = [
            {
                '_op_type': 'index',
                '_index': 'mcs',
                '_type': 'document',
            '_source': set_vendor(m)
            } for m in data
        ]
        osbulk(OpenSearch(**OPENSEARCH_PARAMS), ops)

