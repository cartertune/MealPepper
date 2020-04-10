from pymongo import MongoClient


class MongoConnection:
    def __init__(self):
        client = MongoClient()
        self.db = client.meal_planner_db


    def get_collection(self, collection_name):
        return self.db[collection_name]


mongo_connection = MongoConnection()
