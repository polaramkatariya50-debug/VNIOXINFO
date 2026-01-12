from telegram import ReplyKeyboardMarkup
from config import OWNER_IDS

def main_menu(uid):
    kb = [
        ["📂 GET INFORMATION"],
        ["🛒 GET API"],
        ["🎁 REFER & EARN"]
    ]
    if uid in OWNER_IDS:
        kb.append(["🔐 OWNER PANEL"])
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

INFO_MENU = ReplyKeyboardMarkup(
    [
        ["📱 INDIA NUMBER INFO", "🇵🇰 PAKISTAN NUMBER INFO"],
        ["🚘 VEHICLE → INFORMATION", "🚗 VEHICLE → OWNER NUMBER"],
        ["🎮 FREE FIRE UID INFO", "🪪 AADHAAR / FAMILY INFO"],
        ["🏦 IFSC INFO", "📡 CALL TRACE INFO"],
        ["💳 FAMPAY INFO"],
        ["⬅️ BACK"]
    ],
    resize_keyboard=True
)
