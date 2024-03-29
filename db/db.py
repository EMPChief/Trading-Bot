from pymongo import MongoClient, errors
from constants.defs import MONGO_CONNECTION_STRING

class DataBaseMongo:
    LEARNING_COLLECTION = "forex_sample"
    FOREX_CALENDAR = "forex_calender"
    INSTRUMENT_COLLECTION = "forex_instruments"

    def __init__(self):
        self.client = MongoClient(MONGO_CONNECTION_STRING)
        self.db = self.client.forex_learning

    def test_connection(self):
        print(self.db.list_collection_names())

    def add_one(self, collection, document):
        try:
            _ = self.db[collection].insert_one(document)
        except errors.InvalidOperation as e:
            print(f"add_one error: {e}")
            return

    def add_many(self, collection, documents):
        try:
            _ = self.db[collection].insert_many(documents)
        except errors.InvalidOperation as e:
            print(f"add_many error: {e}")
            return

    def query_all(self, collection, **kwargs):
        try:
            data = []
            results = self.db[collection].find(kwargs, {'_id': 0})
            for item in results:
                data.append(item)
            return data
        except errors.InvalidOperation as error:
            print("query_all error:", error)

    def query_single(self, collection, **kwargs):
        try:
            result = self.db[collection].find_one(kwargs, {'_id': 0})
            return result
        except errors.InvalidOperation as error:
            print("query_single error:", error)

    def query_distinct(self, collection, key):
        try:            
            return self.db[collection].distinct(key)
        except errors.InvalidOperation as error:
            print("query_distinct error:", error)
    
    def delete_many(self, collection, **kwargs):
        try:
            return self.db[collection].delete_many(kwargs)
        except errors.InvalidOperation as error:
            print("delete_many error:", error)
    
    def delete_one(self, collection, **kwargs):
        try:
            return self.db[collection].delete_one(kwargs)
        except errors.InvalidOperation as error:
            print("delete_one error:", error)
