from telegram import Update
from telegram.ext import *
from config import BOT_TOKEN, BLOCKED_GROUP_IDS, OWNER_IDS
from keyboards import main_menu, INFO_MENU
from apis import *
from utils import save_txt
from db import ensure_user, users

# ================= API MAP =================

API_MAP = {
    "📱 INDIA NUMBER INFO": api_india_number,
    "🇵🇰 PAKISTAN NUMBER INFO": api_pak_number,
    "🚘 VEHICLE → INFORMATION": api_vehicle_info,
    "🚗 VEHICLE → OWNER NUMBER": api_vehicle_num,
    "🎮 FREE FIRE UID INFO": api_ff,
    "🪪 AADHAAR / FAMILY INFO": api_id_family,
    "🏦 IFSC INFO": api_ifsc,
    "📡 CALL TRACE INFO": api_calltrace,
    "💳 FAMPAY INFO": api_fampay,
}

# ================= HELPERS =================

def is_blocked(update: Update):
    return update.effective_chat.id in BLOCKED_GROUP_IDS

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_blocked(update):
        return

    uid = update.effective_user.id
    ensure_user(uid)

    text = (
        "✨ VNIOXINFO – OSINT BOT\n\n"
        "📂 GET INFORMATION – All OSINT APIs\n"
        "🛒 GET API – Buy / Custom Bot\n"
        "🎁 REFER & EARN – Earn Credits\n"
        "🔐 OWNER PANEL – Admin Tools\n\n"
        "👇 Select option:"
    )

    await update.message.reply_text(text, reply_markup=main_menu(uid))

# ================= HANDLER =================

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_blocked(update):
        return

    uid = update.effective_user.id
    txt = update.message.text.strip()

    # GET INFORMATION
    if txt == "📂 GET INFORMATION":
        await update.message.reply_text("Select API:", reply_markup=INFO_MENU)
        return

    # GET API
    if txt == "🛒 GET API":
        await update.message.reply_text(
            "🛒 GET API\n\n"
            "• Buy OSINT API\n"
            "• Make Your Own Bot\n\n"
            "Contact: @SUBHXCOSMO"
        )
        return

    # REFER & EARN
    if txt == "🎁 REFER & EARN":
        bot = await context.bot.get_me()
        u = users.find_one({"_id": uid}) or {}
        refs = u.get("ref_count", 0)
        credits = u.get("credits", 0)

        await update.message.reply_text(
            f"🎁 REFER & EARN\n\n"
            f"Your Link:\nhttps://t.me/{bot.username}?start={uid}\n\n"
            f"Referrals: {refs}\n"
            f"Credits: {credits}"
        )
        return

    # OWNER PANEL
    if txt == "🔐 OWNER PANEL":
        if uid not in OWNER_IDS:
            await update.message.reply_text("❌ Access Denied")
            return

        await update.message.reply_text(
            "👑 OWNER PANEL\n\n"
            "• Broadcast\n"
            "• Stats\n"
            "• Gift Credits\n"
            "(Coming soon)"
        )
        return

    # API BUTTON CLICK
    if txt in API_MAP:
        context.user_data["api"] = txt
        await update.message.reply_text("✍️ Send input:")
        return

    # API INPUT
    if "api" in context.user_data:
        api_fn = API_MAP[context.user_data["api"]]
        data = api_fn(txt)

        # 🔥 RAW DATA -> TXT
        file_path = save_txt(data)

        await update.message.reply_document(
            document=open(file_path, "rb"),
            caption="📄 RAW API RESPONSE (.txt)"
        )

        context.user_data.clear()
        return

# ================= RUN =================

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
