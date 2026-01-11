from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, ContextTypes, ChatMemberHandler
)
from config import *
from apis import *
from formatters import *
from image_renderer import text_to_image
from pdf_exporter import image_to_pdf
from db import Database
from logger import send_log

db = Database(MONGO_URI, DB_NAME)

def is_owner(uid): return uid in OWNER_IDS

async def check_join(uid, context):
    for cid in MUST_JOIN_CHANNELS:
        try:
            m = await context.bot.get_chat_member(cid, uid)
            if m.status in ("left","kicked"):
                return False
        except:
            return False
    return True

async def must_join(update):
    btn = [[InlineKeyboardButton("🔔 Join", url=l)] for l in MUST_JOIN_CHANNELS.values()]
    btn.append([InlineKeyboardButton("✅ I Joined", callback_data="check_join")])
    await update.message.reply_text(
        "🚫 Bot use karne ke liye sabhi channels join karo",
        reply_markup=InlineKeyboardMarkup(btn)
    )

async def send_image(update, title, data):
    text = fmt_all(title, data)
    img = text_to_image(text)
    pdf = image_to_pdf(img)
    await update.message.reply_photo(photo=open(img,"rb"), caption=title)
    await update.message.reply_document(document=open(pdf,"rb"), filename="OSINT_Report.pdf")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    db.add_user(u.id)
    await send_log(context.bot, f"START\nUser: {u.id} @{u.username}")

    if not await check_join(u.id, context):
        await must_join(update); return

    buttons = [
        [InlineKeyboardButton("📞 Indian Number", callback_data="num")],
        [InlineKeyboardButton("🚗 Vehicle → Owner", callback_data="vehiclenum")],
        [InlineKeyboardButton("🪪 Family / Ration", callback_data="family")],
        [InlineKeyboardButton("🇵🇰 Pakistan Number", callback_data="pk")],
        [InlineKeyboardButton("🚘 RC Info", callback_data="rc")],
        [InlineKeyboardButton("🎮 Free Fire UID", callback_data="ff")],
        [InlineKeyboardButton("🏦 IFSC Info", callback_data="ifsc")],
        [InlineKeyboardButton("📡 Call Trace", callback_data="calltrace")],
        [InlineKeyboardButton("💳 Fampay Info", callback_data="fampay")],
    ]
    if is_owner(u.id):
        buttons.append([InlineKeyboardButton("👑 OWNER PANEL", callback_data="owner")])

    await update.message.reply_text(
        "🔥 OSINT MAIN MENU",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    if q.data == "owner":
        await q.message.reply_text(
            "👑 OWNER PANEL",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📣 GLOBAL BROADCAST", callback_data="gcast")]
            ])
        )
        return
    await q.message.reply_text(f"Usage:\n/{q.data} <value>")

async def num(update, c): await send_image(update,"INDIAN NUMBER INFO",api_num(c.args[0]))
async def vehiclenum(update, c): await send_image(update,"VEHICLE NUM TO OWNER",api_vehicle_num(c.args[0]))
async def family(update, c): await send_image(update,"RATION CARD FAMILY",api_id_family(c.args[0]))
async def pk(update, c): await send_image(update,"PAKISTAN NUMBER",api_pk(c.args[0]))
async def rc(update, c): await send_image(update,"RC INFO",api_rc(c.args[0]))
async def ff(update, c): await send_image(update,"FREE FIRE UID",api_ff(c.args[0]))
async def ifsc(update, c): await send_image(update,"IFSC INFO",api_ifsc(c.args[0]))
async def calltrace(update, c): await send_image(update,"CALL TRACE",api_calltrace(c.args[0]))
async def fampay(update, c): await send_image(update,"FAMPAY INFO",api_fampay(c.args[0]))

async def gcast(update, context):
    if not is_owner(update.effective_user.id): return
    msg = " ".join(context.args)
    for u in db.get_users():
        try: await context.bot.send_message(u, msg)
        except: pass
    await send_log(context.bot, f"GLOBAL BROADCAST\nBy {update.effective_user.id}")

async def bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member.new_chat_member.status == "member":
        u = update.effective_user; chat = update.effective_chat
        await context.bot.send_message(
            chat.id,
            f"👋 Hello {chat.title}\n🤖 OSINT Bot Activated\nAdded by @{u.username or u.first_name}"
        )
        await send_log(context.bot, f"BOT ADDED\nBy {u.id}\nChat {chat.id}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu))
    app.add_handler(ChatMemberHandler(bot_added, ChatMemberHandler.MY_CHAT_MEMBER))

    app.add_handler(CommandHandler("num", num))
    app.add_handler(CommandHandler("vehiclenum", vehiclenum))
    app.add_handler(CommandHandler("family", family))
    app.add_handler(CommandHandler("pk", pk))
    app.add_handler(CommandHandler("rc", rc))
    app.add_handler(CommandHandler("ff", ff))
    app.add_handler(CommandHandler("ifsc", ifsc))
    app.add_handler(CommandHandler("calltrace", calltrace))
    app.add_handler(CommandHandler("fampay", fampay))
    app.add_handler(CommandHandler("gcast", gcast))

    app.run_polling()

if __name__ == "__main__":
    main()
