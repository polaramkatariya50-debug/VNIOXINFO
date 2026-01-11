from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters,
    ChatMemberHandler, CommandHandler
)
from config import *
from apis import *
from formatters import *
from image_renderer import text_to_image
from pdf_exporter import image_to_pdf
from db import Database
from logger import send_log

db = Database(MONGO_URI, DB_NAME)

# ---------- HELPERS ----------
def is_owner(uid):
    return uid in OWNER_IDS

async def check_join(uid, context):
    for cid in MUST_JOIN_CHANNELS:
        try:
            m = await context.bot.get_chat_member(cid, uid)
            if m.status in ("left", "kicked"):
                return False
        except:
            return False
    return True

async def must_join(update):
    btn = [[InlineKeyboardButton("🔔 Join", url=l)] for l in MUST_JOIN_CHANNELS.values()]
    await update.message.reply_text(
        "🚫 Bot use karne ke liye sabhi channels join karo",
        reply_markup=InlineKeyboardMarkup(btn)
    )

async def send_result(update, title, data):
    text = fmt_all(title, data)
    img = text_to_image(text)
    pdf = image_to_pdf(img)

    await update.message.reply_photo(photo=open(img, "rb"), caption=title)
    await update.message.reply_document(document=open(pdf, "rb"), filename="OSINT_Report.pdf")

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    db.add_user(u.id)

    await send_log(context.bot, f"START\nUser: {u.id} @{u.username}")

    if not await check_join(u.id, context):
        await must_join(update)
        return

    buttons = [
        [InlineKeyboardButton("📞 Indian Number", callback_data="search:num")],
        [InlineKeyboardButton("🚗 Vehicle → Owner", callback_data="search:veh_owner")],
        [InlineKeyboardButton("🚘 Vehicle → Information", callback_data="search:veh_info")],
        [InlineKeyboardButton("🪪 Family / Ration", callback_data="search:family")],
        [InlineKeyboardButton("🇵🇰 Pakistan Number", callback_data="search:pk")],
        [InlineKeyboardButton("🚘 RC Info", callback_data="search:rc")],
        [InlineKeyboardButton("🎮 Free Fire UID", callback_data="search:ff")],
        [InlineKeyboardButton("🏦 IFSC Info", callback_data="search:ifsc")],
        [InlineKeyboardButton("📡 Call Trace", callback_data="search:trace")],
        [InlineKeyboardButton("💳 Fampay Info", callback_data="search:fampay")],
    ]

    await update.message.reply_text(
        "🔥 OSINT MAIN MENU",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ---------- BUTTON ROUTER ----------
async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    action, key = q.data.split(":")
    if action != "search":
        return

    context.user_data["await"] = key

    examples = {
        "num": "📞 Example:\n9876543210",
        "veh_owner": "🚗 Example:\nUP64AF2215",
        "veh_info": "🚘 Example:\nMH01AB1234",
        "family": "🪪 Example:\n066004120629",
        "pk": "🇵🇰 Example:\n3014819864",
        "rc": "🚘 Example:\nMH01AB1234",
        "ff": "🎮 Example:\n2819649271",
        "ifsc": "🏦 Example:\nSBIN0000001",
        "trace": "📡 Example:\n9876543210",
        "fampay": "💳 Example:\nmouktik0@fam",
    }

    await q.message.reply_text(
        f"{examples.get(key)}\n\n✍️ Now send value:"
    )

# ---------- TEXT INPUT ----------
async def text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key = context.user_data.get("await")
    if not key:
        return

    value = update.message.text.strip()
    context.user_data["await"] = None

    loading = await update.message.reply_text("⏳ Loading, please wait...")

    api_map = {
        "num": api_num,
        "veh_owner": api_vehicle_num,
        "veh_info": api_vehicle_info,
        "family": api_id_family,
        "pk": api_pk,
        "rc": api_rc,
        "ff": api_ff,
        "ifsc": api_ifsc,
        "trace": api_calltrace,
        "fampay": api_fampay,
    }

    data = api_map[key](value)
    await loading.delete()
    await send_result(update, key.upper(), data)

# ---------- BOT ADDED ----------
async def bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member.new_chat_member.status == "member":
        u = update.effective_user
        chat = update.effective_chat
        await context.bot.send_message(
            chat.id,
            f"👋 Hello {chat.title}\n🤖 OSINT Bot Activated\nAdded by @{u.username or u.first_name}"
        )
        await send_log(context.bot, f"BOT ADDED\nBy {u.id}\nChat {chat.id}")

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_input))
    app.add_handler(ChatMemberHandler(bot_added, ChatMemberHandler.MY_CHAT_MEMBER))

    app.run_polling()

if __name__ == "__main__":
    main()
