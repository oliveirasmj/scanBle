import pymongo
from pymongo import MongoClient

cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
#cluster = pymongo.MongoClient("mongodb+srv://linux:1234@cluster0.7kmsjgc.mongodb.net/?retryWrites=true&w=majority")

db = cluster["dbscan"]

collection = db["services"]
collection.delete_many({})

collection = db["devices"]
collection.delete_many({})

cluster.close()
