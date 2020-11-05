import pymongo
from pprint import pprint

from config import DB_NAME, TEST_DB_URI, COL_DRIVERS, COL_ROUTES
from connect import Connect

def get_client_connection():
     client = Connect.get_connection()
     return client

# mydb = client[DB_NAME]
# drivers_col = mydb[COL_DRIVERS]
# cursor = drivers_col.find({})

# for driver in cursor:
#      pprint(driver)
