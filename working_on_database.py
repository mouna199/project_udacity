from pymongo import MongoClient
import pymongo

client = MongoClient()
db = client.osm
my_collection=db.southampton
print my_collection.count()

Cities={	"Southampton":"Southampton",
	"Woolston, Southampton":"Woolston",
	"Thornhill, Southampton":"Thornhill",
	"West End, Southampton":"West End",
	"Marchwood, Southampton":"Marchwood",
	"Bursledon, Southampton":"Bursledon",
	"Nursling, Southampton":"Nursling",
	"Eastleigh":"Eastleigh",
	"Bassett":"Bassett",
	"Southampton`":"Southampton",
	"Bitterne Village, Southampton":"Bitterne Village",
	"Netley Abbey":"Netley Abbey"
            }
def update_city(old_city,new_city):
    db.southampton.update({"address.city": old_city}, {"$set": {"address.city":new_city}},multi=True )

for key,value in Cities.iteritems():
    update_city(key,value)

other_Cities={"Southampton":"Southampton",
	"Southampton, Hampshire, England, UK":"Southampton",
	"Hampshire, England, UK":"Southampton",
	"West End":"West End",
	"Weston Lane":"Weston Lane",
	"Hampshire, England,UK":"Southampton"
}
def update_other(old_city,new_city):
    db.southampton.update({"is_in": old_city}, {"$set": {"address":{"city": new_city}}}, multi=True)
    db.southampton.update({"is_in": old_city}, {"$unset": {"is_in": old_city}}, multi=True)

for key, value in other_Cities.iteritems():
    update_other(key, value)

