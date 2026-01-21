import telebot
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_PROMPT = """
তুমি একজন খুব বুদ্ধিমান, বন্ধুসুলভ মানুষসুলভ সহকারী।

নিয়ম:
- ব্যবহারকারী English লিখলে → সুন্দর ও স্বাভাবিক বাংলায় উত্তর দেবে
- Bangla, Hindi, Nepali লিখলেও → বাংলায় উত্তর দেবে
- মানুষের মতো করে কথা বলবে
- কখনো বলবে না “আমি একটি AI মডেল / প্রোগ্রাম”
- উত্তর হবে পরিষ্কার, কাজে লাগার মতো, উদাহরণসহ
- অহেতুক লম্বা বা রোবট টাইপ কথা বলবে না

তোমার নাম: GM Assistant
"""

def ai_reply(text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "temperature": 0.8,
        "max_tokens": 600
    }

    try:
        r = requests.post(url, headers=headers, json=data, timeout=60)
        res = r.json()
        return res["choices"][0]["message"]["content"]
    except Exception as e:
        print("ERROR:", e)
        return "এখন একটু সমস্যা হচ্ছে, একটু পর আবার লিখো 🙂"


@bot.message_handler(commands=["start"])
def start(m):
    bot.reply_to(m,
        "👋 হ্যালো!\n"
        "আমি GM Assistant.\n\n"
        "তুমি Bangla / English / Hindi / Nepali যেকোনো ভাষায় লিখতে পারো।\n"
        "English লিখলেও আমি বাংলায় বুঝিয়ে বলবো 🙂\n\n"
        "যা খুশি লিখে শুরু করো।"
    )


@bot.message_handler(func=lambda m: True)
def chat(m):
    bot.send_chat_action(m.chat.id, 'typing')
    reply = ai_reply(m.text)
    bot.reply_to(m, reply)


print("🤖 GM Assistant is running...")
bot.infinity_polling()
