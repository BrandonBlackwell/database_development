import pymysql
import hashlib

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
    def __init__(self, mongo_doc=None, data_map=None, host="localhost", user="root", database="dev_dummy"):
        self.mongo_doc  = mongo_doc
        self.connection = pymysql.connect(host=host, user=user, database=database)
        self.curs       = self.__get_curs()
    data_map = {
        "Name": "name",
        "Age": "age",
        "Gender": "gender",
        "Blood Type": "blood_type",
        "Medical Condition": "medical_condition",
        "Date of Admission": "admission_date",
        "Doctor": "doctor"
    }
    metrics_tuple = []
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
    
    def clean(self, json_obj):
        updated_json = {"metrics":[], "units":[], "values":[]}
        for k,v in json_obj.items():
            if k[-4:] == "Unit":
                updated_json["metrics"] += [self.metrics_map[k]]
                updated_json["units"] += [v]
            elif k[-5:] == "Value":
                updated_json["values"] += [v]
        for i in range(len(updated_json["metrics"])):
            self.metrics_tuple = (updated_json["metrics"][i],updated_json["units"][i],updated_json["values"][i])
        return updated_json
    
    def insert_into_dim(self, table, fields, values):
        placeholder = ", ".join(["%s"]*len(fields))
        query = f"INSERT INTO {table} ({fields}) VALUES ({placeholder});"
        self.curs.executemany(query,values)
    def migrate(self,json_obj):
        pass
            # For late arriving dimensions
            # Solution 1: Use a standardized default dummy value. Now we'd
            # be able to compare the values to the set of dummy values.
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