import telebot
import requests
import re

# توكن البوت
API_TOKEN = "7756130100:AAEZAgI4mVZyjV2HulvNtBBZurKhVIDFd-8"
# مفتاح واجهة API للتحقق من الأرقام
ACCESS_KEY = "35aee4b59b91dad0fca3831889371f6e"

bot = telebot.TeleBot(API_TOKEN)

# دالة تحليل الرقم اليمني
def analyze_yemen_number(number):
    try:
        url = f"http://apilayer.net/api/validate?access_key={ACCESS_KEY}&number={number}&country_code=YE&format=1"
        response = requests.get(url).json()

        if response.get("valid"):
            report = f"""
[تقرير استخباراتي خاص - اليمن]
رقم الهاتف: {response['international_format']}
الشبكة: {response['carrier']}
الدولة: {response['country_name']}
النوع: {"موبايل" if response['line_type'] == "mobile" else response['line_type']}
رمز الدولة: {response['country_prefix']}
رمز الشبكة: {number[:5]}
النتيجة: الرقم صالح ونشط ✅

[تحليل خاص]
- الرقم يعمل حاليًا داخل اليمن.
- يمكن توسيع التحليل لربطه بـ WhatsApp / Truecaller.
"""
        else:
            report = "[فشل] الرقم غير صالح أو غير متوفر في اليمن."

    except Exception as e:
        report = f"[خطأ] فشل في التحليل:\n{str(e)}"
    
    return report

# بدء البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "مرحبًا بك في نظام تحليل الأرقام اليمني.\nأرسل رقمًا يبدأ بـ +967 لتحليل استخباراتي.")

# استقبال وتحليل الأرقام
@bot.message_handler(func=lambda message: True)
def analyze_number(message):
    text = message.text.strip()
    match = re.search(r'\+967\d{7,9}', text)
    if match:
        number = match.group()
        result = analyze_yemen_number(number)
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, "يرجى إرسال رقم يمني بصيغة صحيحة، مثال: +9677XXXXXXXX")

bot.remove_webhook()
bot.infinity_polling()
