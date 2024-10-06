import pymongo
from data_migrator import DataMigrator

# # Mongo connection
# client = pymongo.MongoClient("localhost", 27017)
# mongo_db = client.dev_dummy
# collection = mongo_db.healthcare

print("".join(["%s"]*3))

# print(collection.find_one({}))

# json = list(collection.find({}))
# print(len(json))
# data_migrator = DataMigrator(json, data_map)
# data_migrator.test()