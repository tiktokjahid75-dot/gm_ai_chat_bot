import telebot
import requests
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ai_reply(text):
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
                "content": (
                    "You are a smart, friendly AI assistant. "
                    "If user writes English/Hindi/Nepali, first translate to Bangla, "
                    "then give a natural helpful answer in Bangla like ChatGPT."
                )
            },
            {"role": "user", "content": text}
        ],
        "temperature": 0.7,
        "max_tokens": 700
    }

    r = requests.post(url, headers=headers, json=data, timeout=60)
    res = r.json()

    if "choices" not in res:
        print("GROQ ERROR:", res)
        return "⚠️ AI এখন কাজ করছে না। API / Railway variable চেক করো।"

    return res["choices"][0]["message"]["content"]


@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(
        msg,
        "👋 হ্যালো! আমি GM AI Assistant 🤖\n\n"
        "আমি মানুষের মতো করে কথা বলি।\n"
        "👉 English / Hindi / Nepali লিখলে বাংলায় বুঝিয়ে বলবো\n"
        "👉 যেকোনো প্রশ্ন করো\n\n"
        "✍️ এখন কিছু লেখো..."
    )


@bot.message_handler(func=lambda m: True)
def chat(msg):
    try:
        bot.send_chat_action(msg.chat.id, "typing")
        reply = ai_reply(msg.text)
        bot.reply_to(msg, reply)
    except Exception as e:
        print("BOT ERROR:", e)
        bot.reply_to(msg, "⚠️ সার্ভারে সমস্যা হচ্ছে। Railway variables চেক করো।")


print("🤖 Bot running...")
bot.infinity_polling()
