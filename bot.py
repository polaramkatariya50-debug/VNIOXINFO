from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from config import BOT_TOKEN
from apis import *
from formatters import *
from image_renderer import text_to_image
from pdf_exporter import image_to_pdf

# ===== BUTTON MAP =====
BUTTONS = {
    "📱 INDIA NUMBER INFO": ("9876543210", api_india_number, lambda d: fmt_india_number(d)),
    "🎮 FREE FIRE UID INFO": ("2819649271", api_ff, lambda d: fmt_raw("FREE FIRE UID INFO", d)),
    "🇵🇰 PAKISTAN NUMBER INFO": ("3014819864", api_pak_number, lambda d: fmt_raw("PAKISTAN NUMBER INFO", d)),
    "🚗 VEHICLE → OWNER NUMBER": ("UP64AF2215", api_vehicle_num, lambda d: fmt_raw("VEHICLE OWNER NUMBER", d)),
    "🚘 VEHICLE → INFORMATION": ("MH01AB1234", api_vehicle_info, lambda d: fmt_raw("VEHICLE INFORMATION", d)),
    "🪪 AADHAAR / FAMILY INFO": ("066004120629", api_id_family, lambda d: fmt_raw("AADHAAR / FAMILY INFO", d)),
    "🏦 IFSC INFO": ("SBIN0000001", api_ifsc, lambda d: fmt_raw("IFSC INFO", d)),
    "📡 CALL TRACE INFO": ("9876543210", api_calltrace, lambda d: fmt_raw("CALL TRACE INFO", d)),
    "💳 FAMPAY INFO": ("mouktik0@fam", api_fampay, lambda d: fmt_raw("FAMPAY INFO", d)),
}

KEYBOARD = [
    ["🎮 FREE FIRE UID INFO", "📱 INDIA NUMBER INFO"],
    ["🇵🇰 PAKISTAN NUMBER INFO", "🚗 VEHICLE → OWNER NUMBER"],
    ["🚘 VEHICLE → INFORMATION", "🪪 AADHAAR / FAMILY INFO"],
    ["🏦 IFSC INFO", "📡 CALL TRACE INFO"],
    ["💳 FAMPAY INFO"],
]

async def entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "sʜʏᴧᴍ\n\n✨ Welcome to VNIOX OSINT Intelligence System\n🔍 Full HD Image + PDF"
    )
    await update.message.reply_text(
        "👇 Select:",
        reply_markup=ReplyKeyboardMarkup(KEYBOARD, resize_keyboard=True)
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()

    if txt in BUTTONS:
        ex, _, _ = BUTTONS[txt]
        context.user_data["mode"] = txt
        await update.message.reply_text(f"{txt}\n\nExample:\n{ex}\n\n✍️ Send input:")
        return

    mode = context.user_data.get("mode")
    if not mode:
        return

    await update.message.reply_text("⏳ Loading...")
    _, api_fn, fmt_fn = BUTTONS[mode]
    data = api_fn(txt)
    out = fmt_fn(data)

    img = text_to_image(out)
    pdf = image_to_pdf(img)

    await update.message.reply_photo(photo=open(img, "rb"))
    await update.message.reply_document(document=open(pdf, "rb"))
    context.user_data.clear()

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, entry))
    app.add_handler(MessageHandler(filters.TEXT, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
