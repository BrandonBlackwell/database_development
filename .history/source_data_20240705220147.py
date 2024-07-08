import pymongo
import pymysql

client = pymongo.MongoClient("localhost", 27017)
db = client.dev_dummy
