import telebot
import requests
import os
from langdetect import detect

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def translate_to_bn(text):
    try:
        url = "https://libretranslate.com/translate"
        data = {
            "q": text,
            "source": "auto",
            "target": "bn",
            "format": "text"
        }
        r = requests.post(url, data=data, timeout=20)
        return r.json()["translatedText"]
    except:
        return text

def groq_chat(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI. Always reply clearly in Bangla. Do not lie. Do not pretend to be human."
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4
    }

    r = requests.post(url, headers=headers, json=data, timeout=60)
    res = r.json()
    return res["choices"][0]["message"]["content"]

@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, 
    "🤖 GM Free AI Bot\n\n"
    "✔ English → বাংলা অনুবাদ\n"
    "✔ Bangla / Hindi / Nepali বোঝে\n"
    "✔ Normal প্রশ্নের উত্তর দেয়\n\n"
    "👉 যা খুশি লিখো"
    )

@bot.message_handler(func=lambda m: True)
def chat(msg):
    try:
        bot.send_chat_action(msg.chat.id, "typing")

        user_text = msg.text
        lang = detect(user_text)

        if lang != "bn":
            user_text = translate_to_bn(user_text)

        reply = groq_chat(user_text)
        bot.reply_to(msg, reply)

    except Exception as e:
        print("ERROR:", e)
        bot.reply_to(msg, "⚠️ এখন AI কাজ করছে না, পরে চেষ্টা করো।")

print("Bot running...")
bot.infinity_polling()
