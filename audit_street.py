
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import string

OSMFILE = "example.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Rd":"Road",
            "Ave":"Avenue"
            }


def audit_street_type(street_types, street_name):
    #getting the last word of the street
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        # if the street name is something else , then we add it to a list
        if street_type not in expected:
            street_types[street_type].add(street_name)
    
# to get the street name function
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

#opening our file, and setting a street types list
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):

                # if we have a street name then we call the audit type function
                if is_street_name(tag):
                    tag.attrib['v']=update_name(tag.attrib['v'], mapping)
    osm_file.close()
    return street_types


def update_name(name, mapping):
    m=street_type_re.search(name)
    if m :
        street_type=m.group()
    
        if street_type in mapping.keys():
            
            name=string.replace(name,street_type,mapping[street_type])
            #name.replace(street_type,mapping[street_type])
            

    return name


def test():
    st_types = audit(OSMFILE)
    #pprint.pprint(dict(st_types))
    print st_types


if __name__ == '__main__':
    test()
