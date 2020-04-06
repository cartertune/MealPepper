from pymongo import MongoClient


class MongoConnection:
    def __init__(self):
        client = MongoClient()
        self.db = client.test_database
