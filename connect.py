from pymongo import MongoClient, errors
from config import TEST_DB_URI

class Connect(object):
    @staticmethod 
    def get_connection():
        ServerSelectionTimeoutError = errors.ServerSelectionTimeoutError

        try:
            client = MongoClient(
                TEST_DB_URI,
                serverSelectionTimeoutMS=3000
            )
            return client

        except ServerSelectionTimeoutError as e:
            raise ServerSelectionTimeoutError(
                'Error connecting, make sure your IP is whitelisted, changes may take some time to take effect') from e

