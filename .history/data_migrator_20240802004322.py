import pymysql

# Source
# Doc
# Doc clean up
# Parse Doc
# Send data to the correct destination
# Destination

# Mysql connection
# connection = pymysql.connect(host="localhost", user="root", database="dev_dummy")
# curs = connection.cursor()
# sql  = "SHOW COLUMNS FROM dev_dummy.hospital;"
# curs.execute(sql)
# print(curs.fetchall())

# Data Migration Service
class DataMigrator:
    
    doc_tracker = []
    
    def __init__(self, mongo_doc, data_map, host="localhost", user="root", database="dev_dummy"):
        self.mongo_doc  = mongo_doc
        self.data_map   = data_map
        self.connection = pymysql.connect(host, user, database)
        self.curs       = self.__get_curs()
    
    def __get_curs(self):
        return self.connection.cursor()
    
    def test(self, query = "SHOW TABLES;"):
        self.curs.execute(query)
        res = self.curs.fetchall()
        return res
    
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
            
            # Inserting new rows based on 1 or many metric units:
            # Solution 1: Create a counter var or create a list of tuples 
            # [k:v] Create new rows based off counter or len of list. 
            
            # For late arriving dimensions
            # Solution 1: Since every obj has a type we will load a dummy value 
            # in columns where data could possibly be. When the real data is
            # loaded it will have the same doc["_id"] + type. Querying this will
            # get you fact_id to the correct fact row. Use the fact row to update
            # dimension rows that have the dummy values. How do we know dummy
            # values were used in dimensions? 
                # Solution 1: Use a standardized default dummy value. Now we'd
                # be able to compare the values to the set of dummy values.
            pass
# doc = collection.find_one()
# doc = {}
# updated_doc = {}
# for field, val in doc.items():
#     if field == "Hospital":
#         updated_doc.update({"hospital_name":val})
#     elif field == "Doctor":
#         updated_doc.update({"doctor_name":val})
#     elif field == "Room Number":
#         updated_doc.update({"room_number":val})
#     else:
#         updated_doc.update({field:val})
        
# values = [updated_doc["hospital_name"], updated_doc["doctor_name"], updated_doc["room_number"]]

# sql_2 = "INSERT INTO `hospital` (`hospital_name`, `doctor_name`, `room_number`) VALUES (%s, %s, %s)"
# # print(doc)
# curs.execute(sql_2, values)
# connection.commit()
# sql_3 = "SELECT * FROM dev_dummy.hospital;"
# curs.execute(sql_3)
# contents = curs.fetchall()
# print(contents)

metrics_map = {
        "icUnit"           : "ic",
        "jcUnit"           : "jc",
        "normalizedRnUnit" : "normalized_rn"
    }

json_obj = {
    "icUnit": "ohms",
    "icValue": 414.08905,
    "jcUnit": "uA",
    "jcValue": 12.3490,
    "normalizedRnUnit": "A/cm2",
    "normalizedRnValue": 4114.859
}

updated_json = {"metrics":[], "units":[], "values":[]}
for k,v in json_obj.items():
    if k[-4:] == "Unit":
        updated_json["metrics"] += [metrics_map[k]]
        updated_json["units"] += [v]
    elif k[-5:] == "Value":
        updated_json["values"] += [v]


# some code ...
for i in range(len(updated_json["metrics"])):
    metric_tuple = (updated_json["metrics"][i],updated_json["units"][i],updated_json["values"][i])
    # load_fact(...,metric_tuple)
print(updated_json)