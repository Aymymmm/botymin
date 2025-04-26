import telebot
import requests
import re

API_TOKEN = "7756130100:AAEZAgI4mVZyjV2HulvNtBBZurKhVIDFd-8"
PHONE_VERIFY_API = "http://apilayer.net/api/validate"

bot = telebot.TeleBot(API_TOKEN)

def verify_phone(number):
    params = {
        'access_key': '35aee4b59b91dad0fca3831889371f6e',
        'number': number,
        'country_code': '',
        'format': 1
    }
    response = requests.get(PHONE_VERIFY_API, params=params)
    return response.json()

def check_whatsapp(number):
    # مجرد محاكاة ذكية - طريقة عادية تتطلب وسائل متقدمة أكثر لاحقًا
    try:
        if number.startswith('967'):
            number = '+' + number
        url = f"https://api.callmebot.com/whatsapp.php?phone={number}&text=Test&apikey=123456"
        res = requests.get(url)
        return res.status_code != 400
    except:
        return False

def check_facebook(number):
    try:
        url = "https://www.facebook.com/login/identify/?ctx=recover"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        data = {
            "email": number
        }
        res = requests.post(url, headers=headers, data=data)
        return "We've sent you an email" not in res.text
    except:
        return False

def check_instagram(number):
    try:
        url = "https://www.instagram.com/accounts/account_recovery_send_ajax/"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/password/reset/"
        }
        data = {
            "email_or_username": number,
            "recaptcha_challenge_field": ""
        }
        res = requests.post(url, headers=headers, data=data)
        return res.status_code == 200 and '"status":"ok"' in res.text
    except:
        return False

def check_linkedin(number):
    try:
        url = "https://www.linkedin.com/uas/request-password-reset"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        data = {
            "userName": number
        }
        res = requests.post(url, headers=headers, data=data)
        return res.status_code == 200 and "We just emailed a link" not in res.text
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "أرسل رقم الهاتف بالصيغة 777xxxxxx أو 967777xxxxxx:")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    number = message.text.strip()

    if not re.match(r'^(777\d{6}|967777\d{6})$', number):
        bot.send_message(message.chat.id, "❌ رقم غير صحيح. أرسل رقمًا 777xxxxxx أو 967777xxxxxx.")
        return

    bot.send_message(message.chat.id, "جاري تحليل الرقم... انتظر قليلاً.")

    phone_info = verify_phone(number)
    country = phone_info.get('country_name', 'غير معروف')
    carrier = phone_info.get('carrier', 'غير معروف')
    valid = phone_info.get('valid', False)

    whatsapp_active = check_whatsapp(number)
    facebook_exists = check_facebook(number)
    instagram_exists = check_instagram(number)
    linkedin_exists = check_linkedin(number)

    report = f"""🛰️ Yemen BlackBox V2 🛰️

رقم الهاتف: {number}
الدولة: {country}
الشبكة: {carrier}
صحة الخط: {"✅ صالح" if valid else "❌ غير صالح"}

نتائج الاستخبارات:
- واتساب: {"✅ موجود" if whatsapp_active else "❌ غير موجود"}
- فيسبوك: {"✅ موجود" if facebook_exists else "❌ غير موجود"}
- إنستجرام: {"✅ موجود" if instagram_exists else "❌ غير موجود"}
- لينكدإن: {"✅ موجود" if linkedin_exists else "❌ غير موجود"}

- تم بواسطة Yemen BlackBox V2 
"""
    bot.send_message(message.chat.id, report)

bot.remove_webhook()
bot.infinity_polling()