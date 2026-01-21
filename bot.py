import telebot
import requests
import os
import base64

# ===== CONFIG =====
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
তুমি একটি অত্যন্ত বুদ্ধিমান Vision AI।

তুমি English, Bangla, Hindi, Nepali সব ভাষা বুঝতে পারো।
কিন্তু তুমি সব সময় উত্তর শুধু পরিষ্কার বাংলায় দেবে।

যদি ছবি আসে, তাহলে:
- ছবিতে কী আছে বলবে
- এটা কিসের জন্য ব্যবহার হয়
- কী কী করা যেতে পারে
- দরকারি পরামর্শ দেবে

তুমি ChatGPT-এর মতো বন্ধুসুলভভাবে কথা বলবে।
"""

# ===== TEXT AI =====
def ai_text(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 700
    }

    r = requests.post(GROQ_URL, headers=headers, json=data, timeout=60)
    res = r.json()

    if "choices" not in res:
        print(res)
        return "⚠️ AI এখন কাজ করছে না, পরে আবার চেষ্টা করো।"

    return res["choices"][0]["message"]["content"]

# ===== VISION AI =====
def ai_vision(img_b64, caption=""):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.2-11b-vision-preview",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": caption or "এই ছবিটা বিশ্লেষণ করো"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ],
        "max_tokens": 900
    }

    r = requests.post(GROQ_URL, headers=headers, json=data, timeout=120)
    res = r.json()

    if "choices" not in res:
        print(res)
        return "⚠️ ছবি বুঝতে সমস্যা হচ্ছে, পরে আবার পাঠাও।"

    return res["choices"][0]["message"]["content"]

# ===== START =====
@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg,
"""🤖 হ্যালো! আমি Bangla Vision AI Bot

তুমি যেকোনো ভাষায় লেখো  
আমি সব বাংলায় বুঝিয়ে উত্তর দেব।

✍ লেখা পাঠাও  
📸 ছবি পাঠাও → এটা কী, কিসের জন্য, কী করা যায় বলব
""")

# ===== TEXT =====
@bot.message_handler(func=lambda m: m.content_type == "text")
def chat(msg):
    try:
        bot.send_chat_action(msg.chat.id, "typing")
        reply = ai_text(msg.text)
        bot.reply_to(msg, reply)
    except Exception as e:
        print(e)
        bot.reply_to(msg, "⚠️ সার্ভার সমস্যা হচ্ছে, পরে আবার চেষ্টা করো।")

# ===== PHOTO =====
@bot.message_handler(content_types=["photo"])
def photo(msg):
    try:
        bot.send_chat_action(msg.chat.id, "typing")
        file_info = bot.get_file(msg.photo[-1].file_id)
        img = bot.download_file(file_info.file_path)
        b64 = base64.b64encode(img).decode()

        reply = ai_vision(b64, msg.caption or "")
        bot.reply_to(msg, reply)
    except Exception as e:
        print(e)
        bot.reply_to(msg, "⚠️ ছবি বুঝতে পারিনি, আবার পাঠাও।")

print("🤖 Bangla Vision AI Bot running...")
bot.infinity_polling()
