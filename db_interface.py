import pymongo

from config import DB_NAME, TEST_DB_URI, COL_DRIVERS, COL_ROUTES, DB_URI
from connect import Connect

# generally never use globals, except in class projects
CLIENT = Connect.get_connection()
DB = CLIENT[DB_NAME]
DRIVERS_COLLECTION = DB[COL_DRIVERS]
ROUTES_COLLECTION = DB[COL_ROUTES]


def get_client_connection():
    client = Connect.get_connection()
    return client


def add_assignment(assignment):
    driver_id = assignment['driver_id']
    a = assignment.copy()
    del a['driver_id']
    DRIVERS_COLLECTION.update(
        {'_id': driver_id}, {'$push': {'assignments': a}})


def add_driver(driver):
    DRIVERS_COLLECTION.insert_one(driver)


def add_route(route):
    ROUTES_COLLECTION.insert_one(route)


def wipe_database():
    DRIVERS_COLLECTION.remove()
    ROUTES_COLLECTION.remove()
# mydb = client[DB_NAME]
# drivers_col = mydb[COL_DRIVERS]
# cursor = drivers_col.find({})

# for driver in cursor:
#      pprint(driver)
