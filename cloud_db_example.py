import pymongo
from config import DB_NAME, TEST_DB_URI, COL_DRIVERS, COL_ROUTES

ServerSelectionTimeoutError = pymongo.errors.ServerSelectionTimeoutError

# connect to the db using test_user
# test_user only has read access
try:
    client = pymongo.MongoClient(
        TEST_DB_URI,
        serverSelectionTimeoutMS=3000
    )

    mydb = client[DB_NAME]
    drivers_col = mydb[COL_DRIVERS]
    print(drivers_col.find_one())

    routes_col = mydb[COL_ROUTES]
    print(routes_col.find_one())


except ServerSelectionTimeoutError as e:
    raise ServerSelectionTimeoutError(
        'Error connecting, make sure your IP is whitelisted, changes may take some time to take effect') from e
