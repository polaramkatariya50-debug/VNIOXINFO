from telegram import Update
from telegram.ext import *
from config import BOT_TOKEN, BLOCKED_GROUP_IDS
from keyboards import *
from apis import *
from formatters import *
from utils import save_txt
from db import ensure_user

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id in BLOCKED_GROUP_IDS:
        return
    ensure_user(update.effective_user.id)
    await update.message.reply_text("Welcome to VNIOX OSINT BOT",
                                    reply_markup=main_menu(update.effective_user.id))

async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "✅ VERIFIED",
        reply_markup=main_menu(update.effective_user.id)
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id in BLOCKED_GROUP_IDS:
        return

    txt = update.message.text

    if txt == "📂 GET INFORMATION":
        await update.message.reply_text("Select:", reply_markup=INFO_MENU)
        return

    if txt in BUTTONS:
        context.user_data["mode"] = txt
        await update.message.reply_text("Send input:")
        return

    if "mode" in context.user_data:
        api, fmt = BUTTONS[context.user_data["mode"]]
        data = api(txt)
        path = save_txt(fmt(data))
        await update.message.reply_document(open(path,"rb"))
        context.user_data.clear()

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify_join"))
app.add_handler(MessageHandler(filters.TEXT, handle))
app.run_polling()
