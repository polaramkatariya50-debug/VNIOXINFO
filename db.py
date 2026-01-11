from pymongo import MongoClient

class Database:
    def __init__(self, uri, name):
        self.client = MongoClient(uri)
        self.db = self.client[name]

    def add_user(self, uid):
        self.db.users.update_one(
            {"_id": uid},
            {"$set": {"_id": uid}},
            upsert=True
        )

    def get_users(self):
        return [u["_id"] for u in self.db.users.find({}, {"_id": 1})]
