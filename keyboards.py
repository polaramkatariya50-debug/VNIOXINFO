from telegram import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from config import OWNER_IDS, MUST_JOIN_CHANNELS

# ===== MAIN MENU =====
def get_main_menu(uid):
    kb = [
        ["📂 GET INFORMATION"],
        ["🛒 GET API"],
        ["🎁 REFER & EARN"]
    ]
    if uid in OWNER_IDS:
        kb.append(["🔐 OWNER PANEL"])
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

# ===== SUB MENUS =====
INFO_MENU = ReplyKeyboardMarkup(
    [
        ["📱 INDIA NUMBER INFO", "🇵🇰 PAKISTAN NUMBER INFO"],
        ["🎮 FREE FIRE UID INFO", "🚘 VEHICLE → INFORMATION"],
        ["🚗 VEHICLE → OWNER NUMBER", "🪪 AADHAAR / FAMILY INFO"],
        ["🏦 IFSC INFO", "📡 CALL TRACE INFO"],
        ["💳 FAMPAY INFO"],
        ["⬅️ BACK"]
    ],
    resize_keyboard=True
)

API_MENU = ReplyKeyboardMarkup(
    [["💰 BUY API"], ["🤖 MAKE OWN BOT"], ["⬅️ BACK"]],
    resize_keyboard=True
)

OWNER_MENU = ReplyKeyboardMarkup(
    [
        ["📢 BROADCAST"],
        ["🎟 CREATE REDEEM"],
        ["📊 STATS"],
        ["🎁 GIFT ALL USERS"],
        ["⬅️ BACK"]
    ],
    resize_keyboard=True
)

# ===== MUST JOIN (2 TOP, 3 MIDDLE, VERIFY LAST) =====
def must_join_keyboard():
    links = list(MUST_JOIN_CHANNELS.values())
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("JOIN", url=links[0]),
                InlineKeyboardButton("JOIN", url=links[1]),
            ],
            [
                InlineKeyboardButton("JOIN", url=links[2]),
                InlineKeyboardButton("JOIN", url=links[3]),
                InlineKeyboardButton("JOIN", url=links[4]),
            ],
            [
                InlineKeyboardButton("VERIFY", callback_data="verify_join")
            ]
        ]
    )
