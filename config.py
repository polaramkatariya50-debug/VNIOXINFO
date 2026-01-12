import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

OWNER_IDS = {6972508083}

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "vni0x"

# MUST JOIN CHANNELS (5)
MUST_JOIN_CHANNELS = {
    1: "https://t.me/+whz_G-xn0KdkZWI1",
    2: "https://t.me/heroku_club",
    3: "https://t.me/NOBITA_SUPPORT",
    4: "https://t.me/OsintInformationGroup",
    5: "https://t.me/+Ah7RcBKx4zQ2YTE1",
}

# 🔴 BLOCKED GROUP (BOT COMPLETELY SILENT)
BLOCKED_GROUP_IDS = {
    -1002363071054
}
