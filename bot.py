from telegram import Update
from telegram.ext import *
from config import BOT_TOKEN, BLOCKED_GROUP_IDS, OWNER_IDS
from keyboards import *
from apis import *
from formatters import *
from utils import save_txt
from db import ensure_user, users

# ================= API BUTTON MAP =================

INFO_BUTTONS = {
    "📱 INDIA NUMBER INFO": (api_india_number, fmt_india_number),
    "🇵🇰 PAKISTAN NUMBER INFO": (api_pak_number, fmt_pakistan_number),
    "🚘 VEHICLE → INFORMATION": (api_vehicle_info, fmt_vehicle_info),
    "🚗 VEHICLE → OWNER NUMBER": (api_vehicle_num, fmt_vehicle_owner_number),
    "🪪 AADHAAR / FAMILY INFO": (api_id_family, fmt_aadhaar_family_info),
    "🎮 FREE FIRE UID INFO": (api_ff, fmt_free_fire_info),
    "🏦 IFSC INFO": (api_ifsc, fmt_ifsc_info),
    "📡 CALL TRACE INFO": (api_calltrace, fmt_call_trace_info),
    "💳 FAMPAY INFO": (api_fampay, fmt_fampay_info),
}

# ================= HELPERS =================

def is_blocked(update: Update):
    chat = update.effective_chat
    return chat and chat.id in BLOCKED_GROUP_IDS

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_blocked(update):
        return

    uid = update.effective_user.id
    ensure_user(uid)

    await update.message.reply_text(
        "✨ *WELCOME TO VNIOXINFO – OSINT BOT*\n\n"
        "👇 Select an option:",
        reply_markup=main_menu(uid),
        parse_mode="Markdown"
    )

# ================= VERIFY =================

async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "✅ VERIFIED SUCCESSFULLY",
        reply_markup=main_menu(update.effective_user.id)
    )

# ================= MESSAGE HANDLER =================

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_blocked(update):
        return

    uid = update.effective_user.id
    txt = update.message.text.strip()

    # ---------- GET INFORMATION ----------
    if txt == "📂 GET INFORMATION":
        await update.message.reply_text(
            "📂 *SELECT INFORMATION TYPE*",
            reply_markup=INFO_MENU,
            parse_mode="Markdown"
        )
        return

    # ---------- GET API ----------
    if txt == "🛒 GET API":
        await update.message.reply_text(
            "🛒 *GET API OPTIONS*\n\n"
            "🔹 Buy API Access\n"
            "🔹 Make Your Own OSINT Bot\n\n"
            "📩 Contact: @SUBHXCOSMO",
            parse_mode="Markdown"
        )
        return

    # ---------- REFER & EARN ----------
    if txt == "🎁 REFER & EARN":
        bot = await context.bot.get_me()
        u = users.find_one({"_id": uid}) or {}
        refs = u.get("ref_count", 0)
        credits = u.get("credits", 0)

        await update.message.reply_text(
            "🎁 *REFER & EARN*\n\n"
            f"🔗 Your Referral Link:\n"
            f"https://t.me/{bot.username}?start={uid}\n\n"
            f"👥 Referrals: {refs}\n"
            f"💰 Credits: {credits}\n\n"
            "🎉 Earn free credits on each referral!",
            parse_mode="Markdown"
        )
        return

    # ---------- OWNER PANEL ----------
    if txt == "🔐 OWNER PANEL":
        if uid not in OWNER_IDS:
            await update.message.reply_text("❌ Access Denied")
            return

        await update.message.reply_text(
            "👑 *OWNER PANEL*\n\n"
            "📢 BROADCAST\n"
            "🎟 CREATE REDEEM\n"
            "📊 STATS\n"
            "🎁 GIFT ALL USERS\n\n"
            "_Commands coming soon_",
            parse_mode="Markdown"
        )
        return

    # ---------- API BUTTON CLICK ----------
    if txt in INFO_BUTTONS:
        context.user_data["mode"] = txt
        await update.message.reply_text(
            f"✍️ *Send input for:* `{txt}`",
            parse_mode="Markdown"
        )
        return

    # ---------- API INPUT ----------
    if "mode" in context.user_data:
        api_fn, fmt_fn = INFO_BUTTONS[context.user_data["mode"]]

        data = api_fn(txt)

        # DEBUG (optional)
        # print("RAW API RESPONSE:", data)

        text = fmt_fn(data)
        file_path = save_txt(text)

        await update.message.reply_document(
            document=open(file_path, "rb"),
            caption="📄 *VNIOX OSINT REPORT*",
            parse_mode="Markdown"
        )

        context.user_data.clear()
        return

# ================= RUN =================

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify_join"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
