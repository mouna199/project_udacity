# -*- coding: utf-8 -*-
import json
import codecs
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.osm
data = json.load(open("southampton.osm.json"))

db.southampton.insert(data)
