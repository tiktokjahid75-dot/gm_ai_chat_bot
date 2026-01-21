import telebot
import requests
import os

# =========================
# 🔑 ENV KEYS (Railway safe)
# =========================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# =========================
# 🧠 SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
তুমি GM Translator।

কঠোর নিয়ম:
- তুমি শুধুমাত্র অনুবাদ করবে
- কোনো প্রশ্নের উত্তর, ব্যাখ্যা, উপদেশ কিছুই দেবে না
- বাড়তি কথা লিখবে না

ভাষা নিয়ম:
- User যদি English লেখে → শুধু পরিষ্কার বাংলায় অনুবাদ করবে
- User যদি Bangla লেখে → শুধু পরিষ্কার English এ অনুবাদ করবে
- User যদি Hindi / Nepali লেখে → বাংলায় অনুবাদ করবে

ফরম্যাট:
শুধু অনুবাদ লিখবে, অন্য কিছু না।
"""

# =========================
# 🤖 GROQ AI FUNCTION
# =========================
def ai_translate(text):
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
        "temperature": 0.2,
        "max_tokens": 300
    }

    r = requests.post(url, headers=headers, json=data, timeout=60)
    res = r.json()

    if "choices" not in res:
        print("GROQ ERROR:", res)
        return "⚠️ অনুবাদ করা যাচ্ছে না"

    return res["choices"][0]["message"]["content"]


# =========================
# 📌 START
# =========================
@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m,
        "🌐 GM Translator Bot\n\n"
        "আমি শুধু অনুবাদ করি:\n"
        "English ↔ Bangla\n"
        "Hindi/Nepali → Bangla\n\n"
        "যা খুশি লিখুন 👇"
    )


# =========================
# 💬 ALL MESSAGE HANDLER
# =========================
@bot.message_handler(func=lambda m: True)
def chat(m):
    try:
        bot.send_chat_action(m.chat.id, 'typing')
        reply = ai_translate(m.text)
        bot.reply_to(m, reply)
    except Exception as e:
        print("ERROR:", e)
        bot.reply_to(m, "⚠️ Server error, পরে চেষ্টা করুন")


# =========================
print("🤖 GM Translator Bot running...")
bot.infinity_polling()
