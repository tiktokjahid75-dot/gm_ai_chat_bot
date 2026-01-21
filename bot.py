import telebot
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_PROMPT = """
You are a smart, friendly AI assistant like ChatGPT.
You understand Bangla, English, Hindi, and Nepali.
If user writes in English, reply in natural Bangla.
Talk like a real helpful human.
Do not say you are a bot unless asked.
Explain clearly and politely.
"""

def ask_groq(message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7,
        "max_tokens": 700
    }

    r = requests.post(url, headers=headers, json=data, timeout=60)
    res = r.json()
    return res["choices"][0]["message"]["content"]

@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg,
        "👋 হ্যালো! আমি GM AI Assistant.\n\n"
        "তুমি Bangla / English / Hindi / Nepali যেকোনো ভাষায় লিখতে পারো।\n"
        "English লিখলেও আমি বাংলায় সুন্দর করে উত্তর দেবো 😄\n\n"
        "✍️ এখন কিছু লিখো..."
    )

@bot.message_handler(func=lambda m: True)
def chat(msg):
    try:
        bot.send_chat_action(msg.chat.id, "typing")
        reply = ask_groq(msg.text)
        bot.reply_to(msg, reply)
    except Exception as e:
        print("ERROR:", e)
        bot.reply_to(msg, "⚠️ এখন AI busy, একটু পরে চেষ্টা করো।")

print("GM AI Bot running...")
bot.infinity_polling()
