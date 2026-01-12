import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from config import BOT_TOKEN, OWNER_IDS, BLOCKED_GROUP_IDS
from keyboards import *
from apis import *
from formatters import *
from utils import text_to_txt_file
from db import ensure_user, users

# ===== SILENT GROUP CHECK =====
def is_blocked_chat(update: Update):
    chat = update.effective_chat
    return chat and chat.id in BLOCKED_GROUP_IDS

# ===== API MAP =====
BUTTONS = {
    "📱 INDIA NUMBER INFO": ("9876543210", api_india_number, fmt_india_number),
    "🇵🇰 PAKISTAN NUMBER INFO": ("3014819864", api_pak_number, fmt_pakistan_number),
    "🎮 FREE FIRE UID INFO": ("2819649271", api_ff, fmt_free_fire_info),
    "🚘 VEHICLE → INFORMATION": ("MH01AB1234", api_vehicle_info, fmt_vehicle_info),
    "🚗 VEHICLE → OWNER NUMBER": ("UP64AF2215", api_vehicle_num, fmt_vehicle_owner_number),
    "🪪 AADHAAR / FAMILY INFO": ("066004120629", api_id_family, fmt_aadhaar_family_info),
    "🏦 IFSC INFO": ("SBIN0000001", api_ifsc, fmt_ifsc_info),
    "📡 CALL TRACE INFO": ("9876543210", api_calltrace, fmt_call_trace_info),
    "💳 FAMPAY INFO": ("mouktik0@fam", api_fampay, fmt_fampay_info),
}

# ===== MUST JOIN CHECK =====
async def check_must_join(bot, uid):
    from config import MUST_JOIN_CHANNELS
    for link in MUST_JOIN_CHANNELS.values():
        try:
            username = link.split("/")[-1].replace("+", "")
            member = await bot.get_chat_member(f"@{username}", uid)
            if member.status in ("left", "kicked"):
                return False
        except:
            return False
    return True

# ===== /START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_blocked_chat(update):
        return

    uid = update.effective_user.id

    if uid not in OWNER_IDS:
        joined = await check_must_join(context.bot, uid)
        if not joined:
            await update.message.reply_text(
                "🔐 *ACCESS LOCKED*\n\n"
                "Join all channels & tap VERIFY",
                reply_markup=must_join_keyboard(),
                parse_mode="Markdown"
            )
            return

    ensure_user(uid)
    await update.message.reply_text(
        "✨ Welcome to VNIOX OSINT BOT",
        reply_markup=get_main_menu(uid)
    )

# ===== VERIFY CALLBACK =====
async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat and update.effective_chat.id in BLOCKED_GROUP_IDS:
        return

    q = update.callback_query
    uid = q.from_user.id
    await q.answer()

    joined = await check_must_join(context.bot, uid)
    if not joined:
        await q.message.reply_text(
            "❌ Join all channels first",
            reply_markup=must_join_keyboard()
        )
        return

    ensure_user(uid)
    await q.message.reply_text(
        "✅ VERIFIED",
        reply_markup=get_main_menu(uid)
    )

# ===== MESSAGE HANDLER =====
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_blocked_chat(update):
        return

    uid = update.effective_user.id
    txt = update.message.text.strip()

    if txt == "📂 GET INFORMATION":
        await update.message.reply_text("Select API:", reply_markup=INFO_MENU)
        return

    if txt == "🛒 GET API":
        await update.message.reply_text("API OPTIONS:", reply_markup=API_MENU)
        return

    if txt == "🎁 REFER & EARN":
        bot = await context.bot.get_me()
        u = users.find_one({"_id": uid})
        await update.message.reply_text(
            f"🎁 REFER & EARN\n\n"
            f"https://t.me/{bot.username}?start={uid}\n\n"
            f"Credits: {u.get('credits',0)}"
        )
        return

    if txt == "🔐 OWNER PANEL" and uid in OWNER_IDS:
        await update.message.reply_text("OWNER PANEL", reply_markup=OWNER_MENU)
        return

    if txt == "⬅️ BACK":
        await update.message.reply_text("Back", reply_markup=get_main_menu(uid))
        context.user_data.clear()
        return

    if txt in BUTTONS:
        ex, _, _ = BUTTONS[txt]
        context.user_data["mode"] = txt
        await update.message.reply_text(f"{txt}\nExample:\n{ex}\nSend input:")
        return

    mode = context.user_data.get("mode")
    if not mode:
        return

    user = users.find_one({"_id": uid})
    if user.get("credits", 0) <= 0:
        await update.message.reply_text("❌ No credits left")
        return

    _, api_fn, fmt_fn = BUTTONS[mode]
    loop = asyncio.get_running_loop()
    data = await loop.run_in_executor(None, api_fn, txt)

    users.update_one({"_id": uid}, {"$inc": {"credits": -1}})
    file = text_to_txt_file(fmt_fn(data), mode.replace(" ", "_"))
    await update.message.reply_document(open(file, "rb"))

    context.user_data.clear()

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify_join"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
