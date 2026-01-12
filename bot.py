from telegram import Update
from telegram.ext import ContextTypes
from config import BLOCKED_GROUP_IDS
from keyboards import main_menu, must_join_keyboard
from db import ensure_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🔕 Blocked group me bilkul silent
    if update.effective_chat and update.effective_chat.id in BLOCKED_GROUP_IDS:
        return

    uid = update.effective_user.id
    ensure_user(uid)

    welcome_text = (
        "✨ *WELCOME TO VNIOXINFO – OSINT TELEGRAM BOT*\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🚀 *AVAILABLE FEATURES*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📱 Indian Number Lookup\n"
        "🇵🇰 Pakistan Number Lookup\n"
        "🚘 Vehicle Information\n"
        "🚗 Vehicle → Owner Mobile\n"
        "🪪 Aadhaar → Family Info\n"
        "🏦 Bank IFSC Information\n"
        "📡 Indian Call Trace\n"
        "🎮 Free Fire UID Info\n"
        "💳 FamPay Information\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🔐 *SECURITY FEATURES*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✅ Must Join + Verify\n"
        "🔕 Silent in Blocked Groups\n"
        "👑 Owner Control Panel\n\n"
        "👇 *Select an option to continue*"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=main_menu(uid),
        parse_mode="Markdown"
    )


async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🔕 Blocked group me silent
    if update.effective_chat and update.effective_chat.id in BLOCKED_GROUP_IDS:
        return

    await update.callback_query.answer()

    await update.callback_query.message.reply_text(
        "✅ *VERIFICATION SUCCESSFUL*\n\n"
        "Welcome to VNIOXINFO 🎉",
        reply_markup=main_menu(update.effective_user.id),
        parse_mode="Markdown"
    )
