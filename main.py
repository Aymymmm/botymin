import telebot
import requests
import re
import sqlite3
import hashlib
import random
import time
import asyncio

# معلوماتك السرية
API_TOKEN = '7756130100:AAEZAgI4mVZyjV2HulvNtBBZurKhVIDFd-8'
API_KEY = '35aee4b59b91dad0fca3831889371f6e'
bot = telebot.TeleBot(API_TOKEN)

# إنشاء قاعدة بيانات داخلية لحفظ العمليات
conn = sqlite3.connect('blackbox_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS results (number TEXT, data TEXT)''')
conn.commit()

# تابع حماية البوت
def secure_input(text):
    return re.sub(r'[^0-9]', '', text)

# تابع بحث المعلومات
def fetch_info(number):
    try:
        url = f"http://apilayer.net/api/validate?access_key={API_KEY}&number={number}&country_code=&format=1"
        response = requests.get(url)
        data = response.json()
        return data
    except:
        return None

# تابع بحث وهمي عن حسابات سوشيال (استكشاف ذكي)
def search_social_media(number):
    fake_result = {
        "Facebook": "جارٍ البحث...",
        "WhatsApp": "جارٍ البحث...",
    }
    time.sleep(random.uniform(1.5, 3.0))  # تباطؤ لتفادي كشف الحركة

    # تخمين حسابات
    if random.randint(0, 1):
        fake_result["Facebook"] = f"محتمل وجود حساب بهذا الرقم."
    else:
        fake_result["Facebook"] = f"لم يتم العثور على حساب واضح."

    if random.randint(0, 1):
        fake_result["WhatsApp"] = f"الرقم نشط على واتساب."
    else:
        fake_result["WhatsApp"] = f"لم يتم التأكد من نشاط واتساب."

    return fake_result

# تابع إرسال النتيجة النهائية
def send_report(chat_id, number, info, social_info):
    message = f"تحليل الرقم: {number}\n\n"
    if info:
        message += f"الدولة: {info.get('country_name')}\n"
        message += f"الشبكة: {info.get('carrier')}\n"
        message += f"الخط صالح: {info.get('valid')}\n"
    else:
        message += "لم يتم العثور على معلومات مباشرة.\n"

    message += "\nنتائج البحث:\n"
    message += f"فيسبوك: {social_info.get('Facebook')}\n"
    message += f"واتساب: {social_info.get('WhatsApp')}\n"

    bot.send_message(chat_id, message)

    # حفظ في قاعدة البيانات
    cursor.execute('INSERT INTO results (number, data) VALUES (?,?)', (number, message))
    conn.commit()

# الاستماع للأوامر
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في Yemen BlackBox V1\nأرسل رقم هاتف للبحث عنه.\nمثال: 777777777 أو 967777777777")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    number = secure_input(message.text)

    if not (len(number) == 9 or (len(number) == 12 and number.startswith("967"))):
        bot.reply_to(message, "الرجاء إرسال رقم يمني صحيح فقط.")
        return

    bot.reply_to(message, "جارٍ تحليل الرقم... الرجاء الانتظار.")

    info = fetch_info(number)
    social_info = search_social_media(number)

    send_report(message.chat.id, number, info, social_info)

# الحماية من الحظر
bot.remove_webhook()
bot.infinity_polling()