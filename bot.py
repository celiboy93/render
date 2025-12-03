import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Render Environment Variables မှ Key များကို လှမ်းယူပါမည်
# (ကုဒ်ထဲမှာ Key မထည့်ရပါ၊ Render မှာပဲ ထည့်ရပါမယ်)
try:
    API_ID = int(os.environ['API_ID'])
    API_HASH = os.environ['API_HASH']
    SESSION_STRING = os.environ['SESSION_STRING']
    SOURCE_CHANNEL = int(os.environ['SOURCE_CHANNEL'])
    DEST_GROUP = int(os.environ['DEST_GROUP'])
    DELAY_MINUTES = int(os.environ.get('DELAY_MINUTES', 10)) # Default 10 မိနစ်
except KeyError as e:
    print(f"❌ Error: {e} is missing in Environment Variables!")
    exit(1)

# Logging Setup
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

print("🤖 Bot is Starting...")

try:
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
except Exception as e:
    print(f"❌ Login Error: {e}")
    exit(1)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    # Video သို့မဟုတ် File ပါမှ Forward လုပ်မည်
    if event.message.video or event.message.file:
        msg_id = event.message.id
        logger.info(f"📥 New Post Detected! ID: {msg_id}")
        logger.info(f"⏳ Waiting {DELAY_MINUTES} minutes...")
        
        # သတ်မှတ်ချိန် စောင့်ဆိုင်းခြင်း
        await asyncio.sleep(DELAY_MINUTES * 60)
        
        try:
            # Group သို့ Forward လုပ်ခြင်း
            await client.forward_messages(DEST_GROUP, event.message)
            logger.info(f"✅ Forwarded Message {msg_id} to Group!")
        except Exception as e:
            logger.error(f"❌ Forward Error: {e}")

print("✅ Bot Connected & Watching Channel...")
client.start()
client.run_until_disconnected()
