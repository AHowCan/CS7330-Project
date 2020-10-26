import pymongo
from config import LOCAL_URI

myclient = pymongo.MongoClient(LOCAL_URI)
mydb = myclient["mydatabase"]
mycol = mydb["customers"]

mydict = {"name": "John", "address": "Highway 37"}

x = mycol.insert_one(mydict)

print(mycol.find_one())
