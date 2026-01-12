from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

users = db.users

def ensure_user(uid, ref_by=None):
    users.update_one(
        {"_id": uid},
        {"$setOnInsert": {
            "credits": 1,
            "ref_by": ref_by,
            "ref_count": 0
        }},
        upsert=True
    )
