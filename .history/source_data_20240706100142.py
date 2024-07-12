import pymongo
import pymysql

# Mongo connection
client = pymongo.MongoClient("localhost", 27017)
mongo_db = client.dev_dummy
collection = mongo_db.healthcare

# Mysql connection
connection = pymysql.connect(host="localhost", user="root", database="dev_dummy")
curs = connection.cursor()
sql  = "SHOW COLUMNS FROM dev_dummy.hospital;"
curs.execute(sql)
print(curs.fetchall())

# doc = collection.find_one()
# sql_2 = "INSERT INTO `hospital` ()"
# print(doc)
