import pymongo
import pymysql

# Mongo connection
client = pymongo.MongoClient("localhost", 27017)
mongo_db = client.dev_dummy
collection = mongo_db.healthcare

# Mysql connection
connection = pymysql.connect(host="localhost",
                             user="root")
curs = connection.cursor()
sql  = "SHOW DATABASES;"
curs.execute(sql)
result = curs.fetchall()
# print(result)
