from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from config import MUST_JOIN_CHANNELS, OWNER_IDS

def main_menu(uid):
    kb = [["📂 GET INFORMATION"], ["🛒 GET API"], ["🎁 REFER & EARN"]]
    if uid in OWNER_IDS:
        kb.append(["🔐 OWNER PANEL"])
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def info_menu():
    return ReplyKeyboardMarkup(
        [
            ["📱 INDIA NUMBER INFO","🇵🇰 PAK NUMBER INFO"],
            ["🚘 VEHICLE INFO","🚗 VEHICLE OWNER"],
            ["🎮 FREE FIRE","🏦 IFSC"],
            ["📡 CALL TRACE","💳 FAMPAY"],
            ["🪪 AADHAAR FAMILY"],
            ["⬅️ BACK"]
        ],
        resize_keyboard=True
    )

def must_join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("JOIN",url=MUST_JOIN_CHANNELS[0]),
         InlineKeyboardButton("JOIN",url=MUST_JOIN_CHANNELS[1])],
        [InlineKeyboardButton("JOIN",url=MUST_JOIN_CHANNELS[2]),
         InlineKeyboardButton("JOIN",url=MUST_JOIN_CHANNELS[3]),
         InlineKeyboardButton("JOIN",url=MUST_JOIN_CHANNELS[4])],
        [InlineKeyboardButton("VERIFY",callback_data="verify")]
    ])
