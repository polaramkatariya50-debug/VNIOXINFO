from telegram import Update
from telegram.ext import *
from config import BOT_TOKEN, BLOCKED_GROUP_IDS
from keyboards import *
from apis import *
from formatters import *
from utils import save_txt
from db import ensure_user

# ===== API BUTTON MAP =====
BUTTONS = {
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

# ===== /START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🔕 Silent in blocked group
    if update.effective_chat.id in BLOCKED_GROUP_IDS:
        return

    uid = update.effective_user.id
    ensure_user(uid)

    welcome_text = (
        "✨ *WELCOME TO VNIOXINFO – OSINT TELEGRAM BOT*\n\n"
        "🚀 *AVAILABLE FEATURES*\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📱 Indian Number Lookup\n"
        "🇵🇰 Pakistan Number Lookup\n"
        "🚘 Vehicle Information\n"
        "🚗 Vehicle → Owner Mobile\n"
        "🪪 Aadhaar → Family Info\n"
        "🏦 Bank IFSC Information\n"
        "📡 Indian Call Trace\n"
        "🎮 Free Fire UID Info\n"
        "💳 FamPay Information\n\n"
        "🔐 Must Join + Verify System\n"
        "🔕 Silent in Blocked Groups\n"
        "👑 Owner Control Panel\n\n"
        "👇 *Select an option to continue*"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=main_menu(uid),
        parse_mode="Markdown"
    )

# ===== VERIFY CALLBACK =====
async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "✅ *VERIFICATION SUCCESSFUL*\n\nWelcome! 🎉",
        reply_markup=main_menu(update.effective_user.id),
        parse_mode="Markdown"
    )

# ===== MESSAGE HANDLER =====
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🔕 Silent in blocked group
    if update.effective_chat.id in BLOCKED_GROUP_IDS:
        return

    txt = update.message.text.strip()

    # Open information menu
    if txt == "📂 GET INFORMATION":
        await update.message.reply_text(
            "📂 *SELECT INFORMATION TYPE*",
            reply_markup=INFO_MENU,
            parse_mode="Markdown"
        )
        return

    # API button pressed
    if txt in BUTTONS:
        context.user_data["mode"] = txt
        await update.message.reply_text(
            f"✍️ *Send input for:* `{txt}`",
            parse_mode="Markdown"
        )
        return

    # API input received
    if "mode" in context.user_data:
        api_fn, fmt_fn = BUTTONS[context.user_data["mode"]]
        data = api_fn(txt)

        result_text = fmt_fn(data)
        file_path = save_txt(result_text)

        await update.message.reply_document(
            document=open(file_path, "rb"),
            caption="📄 *OSINT REPORT*",
            parse_mode="Markdown"
        )

        context.user_data.clear()

# ===== BOT START =====
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify_join"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
