from datetime import datetime
from config import LOG_CHANNEL_ID

async def send_log(bot, text):
    await bot.send_message(
        chat_id=LOG_CHANNEL_ID,
        text=f"📜 LOG\n{text}\n🕒 {datetime.now()}"
    )
