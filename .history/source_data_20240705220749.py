import pymongo
import pymysql

client = pymongo.MongoClient("localhost", 27017)
mongo_db = client.dev_dummy
collection = mongo_db.healthcare

connection = pymysql.connect(host="localhost",
                             user="root")