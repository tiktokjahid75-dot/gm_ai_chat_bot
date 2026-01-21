import telebot
import requests
import os
from langdetect import detect

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

def translate_to_bn(text):
    url = "https://libretranslate.com/translate"
    data = {
        "q": text,
        "source": "auto",
        "target": "bn",
        "format": "text"
    }
    r = requests.post(url, data=data, timeout=30)
    return r.json()["translatedText"]

@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg,
        "✅ GM Translator Bot\n\n"
        "👉 English / Hindi / Nepali লিখো\n"
        "➡️ আমি শুধু বাংলা অনুবাদ দেবো\n\n"
        "✍️ লেখা শুরু করো"
    )

@bot.message_handler(func=lambda m: True)
def translate(msg):
    try:
        bot.send_chat_action(msg.chat.id, "typing")
        text = msg.text
        lang = detect(text)

        if lang == "bn":
            bot.reply_to(msg, "❗ এটা আগেই বাংলা।")
            return

        bangla = translate_to_bn(text)
        bot.reply_to(msg, bangla)

    except Exception as e:
        print("ERROR:", e)
        bot.reply_to(msg, "⚠️ অনুবাদ করা যাচ্ছে না, পরে চেষ্টা করো।")

print("Translator bot running...")
bot.infinity_polling()
