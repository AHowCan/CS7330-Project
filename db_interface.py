import pymongo

from config import DB_NAME, TEST_DB_URI, COL_DRIVERS, COL_ROUTES
from connect import Connect


def get_client_connection():
    client = Connect.get_connection()
    return client


def add_assignment(assignment):
    print("not implemented")


def add_driver(driver):
    print("not implemented")


def add_route(route):
    print("not implemented")


def wipe_database():
    print("not implemented")
# mydb = client[DB_NAME]
# drivers_col = mydb[COL_DRIVERS]
# cursor = drivers_col.find({})

# for driver in cursor:
#      pprint(driver)
