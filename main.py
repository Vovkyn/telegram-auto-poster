import os
from telethon.sync import TelegramClient
from dotenv import load_dotenv
import openai
import time

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_CHANNELS = os.getenv("TARGET_CHANNELS", "").split(",")

openai.api_key = OPENAI_API_KEY

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

def generate_post_content():
    prompt = "Згенеруй короткий пост для телеграм-каналу про новини відеоігор українською мовою, максимум 400 символів:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=200,
    )
    return response.choices[0].message.content.strip()

async def main():
    content = generate_post_content()
    for channel in TARGET_CHANNELS:
        await client.send_message(channel.strip(), content)

with client:
    client.loop.run_until_complete(main())
