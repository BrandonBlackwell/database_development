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
    
    def get_tables(self):
        query = "SHOW TABLES;"
        self.curs.execute(query)
        tables = self.curs.fetchall()
        return tables or None
    
    def get_columns(self, json_obj, table):
        query = f"SHOW COLUMNS FROM {table};"
        self.curs.execute(query)
        result = self.curs.fetchall()
        columns = [i[0] for i in [tup for tup in result]] or None
        columns_in_json = [self.data_map[k] for k in list(json_obj.keys()) if self.data_map[k] in columns]
        return columns_in_json
                
    
    def get_values(self, json_obj, fields):
        values = []
        for k, v in json_obj.items():
            if self.data_map[k] in fields:
                values.append(v)
        return values
    
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
    
    def insert_into_dim(self, table: str, fields: list, data: list):
        placeholder = ", ".join(["%s"]*len(fields))
        query = f"INSERT INTO {table} ({fields}) VALUES ({placeholder});"
        affected_rows = self.curs.executemany(query, data)
        self.connection.commit()
        return affected_rows
    
    def get_ids(self, table, fields, values):
        query = f"SELECT * FROM {table} WHERE ({fields}) == ({values});"
        self.curs.executemany(query)
        id_tuple = self.curs.fetchall()
        ids = [i[0] for i in [t for t in id_tuple]]
        return ids or None
    
    def insert_into_fact(self, fields, values):
        placeholder = ", ".join(["%s"]*len(fields))
        query = f"INSERT INTO fact ({fields}) VALUES ({placeholder});"
        affected_rows = self.curs.executemany(query, values)
        self.connection.commit()
        return affected_rows
    
    def migrate(self, json_arr):
        tables       = self.get_tables()
        data  = {}
        
        for table in tables:
            data.update({table: []})
        
        for table in tables:  
            for json_obj in json_arr:
                updated_json = self.clean(json_obj)
            
                columns = self.get_columns(json_obj, table)
                values  = self.get_values(json_obj, columns)
                
                data[table] += [values]
                
                self.insert_into_dim(table, columns, values)
            