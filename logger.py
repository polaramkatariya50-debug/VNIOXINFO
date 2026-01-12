from config import LOG_CHANNEL_ID

async def log(bot, text):
    if LOG_CHANNEL_ID:
        await bot.send_message(LOG_CHANNEL_ID, text)
