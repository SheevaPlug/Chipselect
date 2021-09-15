#!/usr/bin/env python
from collections import OrderedDict
from argparse import ArgumentParser

from xmltodict import parse as xmlparse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk as esbulk


def clean_dict(d):
    '''recursively clean the '@' prefixes in attribute names'''
    rv = {}
    for key in d.keys():
        if key.startswith('@'):
            rv[key[1:]] = d[key]
        else:
            rv[key] = d[key]
    d = rv
    rv = {}
    for key in d.keys():
        if type(d[key]) is dict or type(d[key]) is OrderedDict:
            rv[key] = clean_dict(d[key])
        else:
            rv[key] = d[key]
    return rv



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
            devices.append(device)
        else:
            for deviceinfo in deviceinfos:
                device = {}
                device['vendor'] = vendorname
                device.update(clean_dict(deviceinfo))
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
    es = Elasticsearch()
    esbulk(es, ops)
    print('done.')
