import pymongo
import pymysql

# Source
# Doc
# Doc clean up
# Parse Doc
# Send data to the correct destination
# Destination

# Mongo connection
client = pymongo.MongoClient("localhost", 27017)
mongo_db = client.dev_dummy
collection = mongo_db.healthcare

# Mysql connection
connection = pymysql.connect(host="localhost", user="root", database="dev_dummy")
curs = connection.cursor()
# sql  = "SHOW COLUMNS FROM dev_dummy.hospital;"
# curs.execute(sql)
# print(curs.fetchall())

# Data Migration Service
class DataMigrator:
    data_map = {
        "Hospital"    : "hospital_name",
        "Doctor"      : "doctor_name",
        "Room Number" : "room_number"
    }
    doc_tracker = []
    
    def __init__(self, mongo_doc=None, mongo_batch=None):
        self.mongo_doc   = mongo_doc
        self.mongo_batch = mongo_batch
        
    def update_doc(self, orig_doc):
        updated_doc = {}
        for field, val in orig_doc.items():
            if field in self.data_map.keys():
                updated_doc.update({self.data_map[field]:val})
            else:
                updated_doc.update({field:val})
        return updated_doc
    
    def migrate(self,doc):
        if doc["_id"] in self.doc_tracker:
            raise Exception("Document has already been inserted into Maria")
        else:
            # If we insert the document id into the doc tracker before getting approval from Maria
            # it is possible that it did not make there so, after sending to MariaDB 
            # we should wait for approval that it has indeed been inserted and then 
            # insert the doc id into our doc tracker.
            # self.doc_tracker.append(doc["_id"])
            
            # Loading fact table
            # Solution 1: Create a list to keep track of the tables that 
            # are populated. Iterate through list of tables and query for their
            # (natural key + value) which is doc["_id"]+icUnit
            # Maybe use a hash for this or composite key.
            
            # Solution 2:
            pass
doc = collection.find_one()
updated_doc = {}
for field, val in doc.items():
    if field == "Hospital":
        updated_doc.update({"hospital_name":val})
    elif field == "Doctor":
        updated_doc.update({"doctor_name":val})
    elif field == "Room Number":
        updated_doc.update({"room_number":val})
    else:
        updated_doc.update({field:val})
        
values = [updated_doc["hospital_name"], updated_doc["doctor_name"], updated_doc["room_number"]]

sql_2 = "INSERT INTO `hospital` (`hospital_name`, `doctor_name`, `room_number`) VALUES (%s, %s, %s)"
# print(doc)
curs.execute(sql_2, values)
connection.commit()
sql_3 = "SELECT * FROM dev_dummy.hospital;"
curs.execute(sql_3)
contents = curs.fetchall()
print(contents)