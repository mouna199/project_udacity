#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from audit_street import update_name

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]
mapping = {"St": "Street",
           "St.": "Street",
           "Rd": "Road",
           "Ave": "Avenue"
           }


def shape_element(element):
    node = {}
    created = {}
    address = {}
    if element.tag == "node" or element.tag == "way":
        if element.tag == "way":
            node_refs = []
            for nd in element.iter("nd"):
                node_refs.append(nd.get('ref'))
                node["node_refs"] = node_refs
        elif element.tag == "node":
            pos = []
            pos.append(element.get('lat'))
            pos.append(element.get('lon'))
            node['pos'] = pos
        for dkey, dval in element.items():
            if problemchars.search(dval):
                pass
            elif dkey in CREATED:
                created[dkey] = dval
                node["created"] = created.copy()
            else:
                node[dkey] = element.get(dkey)
                node["type"] = element.tag
        for tag in element.iter("tag"):
            if problemchars.search(tag.attrib["k"]):
                pass
            #elif tag.attrib["k"].startswith("is_in"):
               # tag.attriv["k"]="city"
            elif tag.attrib["k"].startswith("addr:"):
                if tag.attrib["k"].startswith("addr:street"):
                    tag.attrib["v"] = update_name(tag.attrib["v"], mapping)
                    # print set(tag.attrib['v'])
                if tag.attrib["k"].count(":") == 1:
                    tag.attrib["k"] = tag.attrib["k"].replace("addr:", "")
                    address[tag.attrib["k"]] = tag.attrib["v"]
                    node["address"] = address.copy()
                else:
                    pass
                    # tag.attrib["v"]=""
                    # tag.attrib["k"]=tag.attrib["k"].replace("addr:","adress:")
            # if tag==

            else:
                node[tag.attrib["k"]] = tag.attrib["v"]

        return node
    else:
        return None



def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        fo.write("[")
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                fo.write(json.dumps(el)+"," + "\n")
        fo.write("]")
# make sure please to delete ',' from the end of the osm file or the insertion of the data into mongodb won't work
    return data


def test():
    data = process_map('southampton.osm', True)

if __name__ == "__main__":
    test()
