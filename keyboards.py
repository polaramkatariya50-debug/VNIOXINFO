from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_IDS, MUST_JOIN_CHANNELS

# ================= MAIN MENU =================

def main_menu(uid):
    keyboard = [
        ["📂 GET INFORMATION"],
        ["🛒 GET API"],
        ["🎁 REFER & EARN"]
    ]

    if uid in OWNER_IDS:
        keyboard.append(["🔐 OWNER PANEL"])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ================= INFORMATION MENU =================

INFO_MENU = ReplyKeyboardMarkup(
    [
        ["📱 INDIA NUMBER INFO", "🇵🇰 PAKISTAN NUMBER INFO"],
        ["🚘 VEHICLE → INFORMATION", "🚗 VEHICLE → OWNER NUMBER"],
        ["🪪 AADHAAR / FAMILY INFO", "🎮 FREE FIRE UID INFO"],
        ["🏦 IFSC INFO", "📡 CALL TRACE INFO"],
        ["💳 FAMPAY INFO"],
        ["⬅️ BACK"]
    ],
    resize_keyboard=True
)


# ================= MUST JOIN KEYBOARD =================

def must_join_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("JOIN", url=MUST_JOIN_CHANNELS[0]),
                InlineKeyboardButton("JOIN", url=MUST_JOIN_CHANNELS[1]),
            ],
            [
                InlineKeyboardButton("JOIN", url=MUST_JOIN_CHANNELS[2]),
                InlineKeyboardButton("JOIN", url=MUST_JOIN_CHANNELS[3]),
                InlineKeyboardButton("JOIN", url=MUST_JOIN_CHANNELS[4]),
            ],
            [
                InlineKeyboardButton("VERIFY", callback_data="verify_join")
            ]
        ]
    )
