import pymongo
from data_migrator import DataMigrator

# Mongo connection
client = pymongo.MongoClient("localhost", 27017)
mongo_db = client.dev_dummy
collection = mongo_db.healthcare

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

# print(collection.find_one({}))

# json = list(collection.find({}))
# print(len(json))
# data_migrator = DataMigrator(json, data_map)
# data_migrator.test()