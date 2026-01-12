from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

users = db.users
logs = db.logs

def ensure_user(uid):
    users.update_one(
        {"_id": uid},
        {"$setOnInsert": {"credits": 0}},
        upsert=True
    )
