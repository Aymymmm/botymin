import telebot
import requests
import os

API_TOKEN = os.getenv("API_TOKEN")
NUMVERIFY_API = os.getenv("NUMVERIFY_API")

bot = telebot.TeleBot(API_TOKEN)

# تحليل رقم الهاتف باستخدام NumVerify
def analyze_number(number):
    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API}&number={number}&format=1"
    response = requests.get(url)
    data = response.json()
    result = ""

    if data.get("valid"):
        result += f"الرقم صحيح ✅\n"
        result += f"الدولة: {data.get('country_name')}\n"
        result += f"شركة الاتصالات: {data.get('carrier')}\n"
        result += f"النوع: {'جوال' if data.get('line_type') == 'mobile' else 'أرضي'}\n"
    else:
        result += "الرقم غير صحيح أو لا يوجد معلومات."

    return result

# فحص Telegram
def check_telegram(number):
    tg_link = f"https://t.me/{number}"
    return f"Telegram: جرّب فتح الرابط:\n{tg_link}"

# فحص WhatsApp
def check_whatsapp(number):
    wa_link = f"https://wa.me/{number.replace('+','')}"
    return f"WhatsApp: افتح الرابط:\n{wa_link}"

# فحص Facebook
def check_facebook(number):
    fb_link = f"https://www.facebook.com/login/identify/?ctx=recover&lwv=110&email={number}"
    return f"Facebook: تحقق من هنا:\n{fb_link}"

# عند استقبال رقم
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    number = message.text.strip()

    if not number.startswith("+"):
        bot.reply_to(message, "أرسل الرقم مع رمز الدولة مثال: +967777777777")
        return

    info = analyze_number(number)
    telegram_check = check_telegram(number)
    whatsapp_check = check_whatsapp(number)
    facebook_check = check_facebook(number)

    full_report = f"{info}\n\n{telegram_check}\n\n{whatsapp_check}\n\n{facebook_check}"
    bot.send_message(message.chat.id, full_report)

# لتشغيل البوت
bot.delete_webhook(drop_pending_updates=True)
bot.infinity_polling(skip_pending=True)
