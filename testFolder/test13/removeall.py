import pymongo
from pymongo import MongoClient

cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")

db = cluster["dbscan"]

collection = db["services"]
collection.delete_many({})

collection = db["devices"]
collection.delete_many({})

cluster.close()
