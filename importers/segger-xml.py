#!/usr/bin/env python
from collections import OrderedDict
from argparse import ArgumentParser

from xmltodict import parse as xmlparse
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk as osbulk

OPENSEARCH_PARAMS = {
    'hosts': [{'host': 'localhost', 'port': 9200}], 
    'http_auth': ('admin', 'admin'),
    'use_ssl': True,
    'verify_certs': False,
    'ssl_show_warn': False,
}


def clean_dict(d):
    '''recursively clean the '@' prefixes in attribute names'''
    rv = {}
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
    return rv

def clean_aliasinfo(data):
    if 'AliasInfo' in data.keys():
        if type(data['AliasInfo']) is list:
            aliases = [d.get('Name') for d in data['AliasInfo']]
        elif type(data['AliasInfo']) is dict:
            aliases = [data['AliasInfo'].get('Name', '')]
        data['AliasInfo'] = aliases
    return data


if __name__ == '__main__':
    parser = ArgumentParser(description='read SEGGER XML file')
    parser.add_argument('infile', help='the SEGGER XML file')
    args = parser.parse_args()

    with open(args.infile, 'r') as ifh: data = xmlparse(ifh.read())

    vendors = data['DeviceDatabase']['VendorInfo']
    devices = []
    for vendor in vendors:
        vendorname = vendor['@Name']
        deviceinfos = vendor['DeviceInfo']
        if type(deviceinfos) is OrderedDict:
            device = {}            
            device['vendor'] = vendorname
            device.update(clean_dict(deviceinfos))
            device = clean_aliasinfo(device)
            devices.append(device)
        else:
            for deviceinfo in deviceinfos:
                device = {}
                device['vendor'] = vendorname
                device.update(clean_dict(deviceinfo))
                device = clean_aliasinfo(device)
                devices.append(device)
    #
    ops = []
    for device in devices:
        ops.append(
            {
                '_op_type': 'index',
                '_index': 'mcs',
                '_type': 'document',
                '_source': device
            }
        )
        pass
    osbulk(OpenSearch(**OPENSEARCH_PARAMS), ops)
