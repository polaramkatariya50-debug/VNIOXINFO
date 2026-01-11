from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ChatMemberHandler,
    CommandHandler,
)
from config import *
from apis import *
from formatters import *
from image_renderer import text_to_image
from pdf_exporter import image_to_pdf
from db import Database
from logger import send_log

# ================= DATABASE =================
db = Database(MONGO_URI, DB_NAME)

# ================= HELPERS =================
def is_owner(uid: int) -> bool:
    return uid in OWNER_IDS


async def check_join(uid: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    for cid in MUST_JOIN_CHANNELS:
        try:
            member = await context.bot.get_chat_member(cid, uid)
            if member.status in ("left", "kicked"):
                return False
        except Exception:
            return False
    return True


async def must_join(update: Update):
    buttons = [
        [InlineKeyboardButton("🔔 Join Channel", url=url)]
        for url in MUST_JOIN_CHANNELS.values()
    ]
    await update.message.reply_text(
        "🚫 Bot use karne ke liye pehle sabhi channels join karo:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


async def send_result(update: Update, title: str, data: dict):
    text = fmt_all(title, data)
    img_path = text_to_image(text)
    pdf_path = image_to_pdf(img_path)

    await update.message.reply_photo(
        photo=open(img_path, "rb"),
        caption=f"📄 {title}",
    )
    await update.message.reply_document(
        document=open(pdf_path, "rb"),
        filename="OSINT_Report.pdf",
    )

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id)

    await send_log(
        context.bot,
        f"START\nUser ID: {user.id}\nUsername: @{user.username}",
    )

    if not await check_join(user.id, context):
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
        "🔥 **VNIOX OSINT PANEL**\n\nSelect an option:",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown",
    )

# ================= BUTTON ROUTER =================
async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if context.user_data is None:
        context.user_data = {}

    try:
        action, key = query.data.split(":")
    except ValueError:
        return

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

    await query.message.reply_text(
        f"{examples.get(key, '✍️ Send input value')}\n\n✍️ Now send value:"
    )

# ================= TEXT INPUT HANDLER =================
async def text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # SAFETY: ensure user_data exists
    if context.user_data is None:
        context.user_data = {}

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

    try:
        data = api_map[key](value)
        await loading.delete()
        await send_result(update, key.upper(), data)
    except Exception as e:
        await loading.edit_text(f"❌ Error: {e}")

# ================= BOT ADDED TO GROUP =================
async def bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member.new_chat_member.status == "member":
        user = update.effective_user
        chat = update.effective_chat

        await context.bot.send_message(
            chat.id,
            f"👋 Hello {chat.title}\n\n"
            f"🤖 VNIOX OSINT Bot Activated\n"
            f"➕ Added by @{user.username or user.first_name}",
        )

        await send_log(
            context.bot,
            f"BOT ADDED\nBy: {user.id}\nChat ID: {chat.id}",
        )

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_input))
    app.add_handler(ChatMemberHandler(bot_added, ChatMemberHandler.MY_CHAT_MEMBER))

    print("🤖 VNIOX OSINT Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
