import pymongo
import sys
sys.path.append("..")
from source_data import DataMigrator

# Mongo connection
client = pymongo.MongoClient("localhost", 27017)
mongo_db = client.dev_dummy
collection = mongo_db.healthcare

json = list(collection.find({}))
print(len(json))
data_migrator = DataMigrator(json)