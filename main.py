import telebot
import requests
import re
import hashlib

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
        headers = {"User-Agent": "Mozilla/5.0"}
        data = {"email": number}
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
        data = {"email_or_username": number}
        res = requests.post(url, headers=headers, data=data)
        return res.status_code == 200 and '"status":"ok"' in res.text
    except:
        return False

def check_linkedin(number):
    try:
        url = "https://www.linkedin.com/uas/request-password-reset"
        headers = {"User-Agent": "Mozilla/5.0"}
        data = {"userName": number}
        res = requests.post(url, headers=headers, data=data)
        return res.status_code == 200 and "We just emailed a link" not in res.text
    except:
        return False

def find_email_from_leaks(number):
    hashed_number = hashlib.sha1(number.encode()).hexdigest()
    leaked_db = {
        "f1d2d2f924e986ac86fdf7b36c94bcdf32beec15": "example@email.com"
    }
    return leaked_db.get(hashed_number, None)

def guess_yahoo_email(number):
    """تخمين ذكي لبريد ياهو من الرقم"""
    possible_email = f"{number}@yahoo.com"
    return possible_email

def is_valid_yemeni_number(number):
    return re.match(r'^(7[0137]\d{7})$', number)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "أرسل رقم الهاتف اليمني بالصيغة: 73xxxxxxx أو 71xxxxxxx أو 70xxxxxxx أو 77xxxxxxx:")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    number = message.text.strip()

    if not is_valid_yemeni_number(number):
        bot.send_message(message.chat.id, "❌ رقم غير صحيح. يجب أن يكون رقم يمني صحيح مكون من 9 أرقام ويبدأ بـ (73 / 71 / 70 / 77).")
        return

    full_number = "967" + number
    bot.send_message(message.chat.id, "جارٍ التحليل الإستخباراتي العميق... ⏳")

    phone_info = verify_phone(full_number)
    country = phone_info.get('country_name', 'غير معروف')
    carrier = phone_info.get('carrier', 'غير معروف')
    valid = phone_info.get('valid', False)

    if country != "Yemen":
        bot.send_message(message.chat.id, "❌ الرقم ليس من اليمن. أرسل رقمًا يمنيًا فقط.")
        return

    whatsapp_active = check_whatsapp(full_number)
    facebook_exists = check_facebook(full_number)
    instagram_exists = check_instagram(full_number)
    linkedin_exists = check_linkedin(full_number)
    leaked_email = find_email_from_leaks(full_number)
    yahoo_email = guess_yahoo_email(number)

    risk_score = sum([whatsapp_active, facebook_exists, instagram_exists, linkedin_exists])

    secret_tag = "⚡ خطر مرتفع" if risk_score >= 3 else "✅ عادي"

    report = f"""🛰️ Yemen BlackBox V4 🛰️

رقم الهاتف: {full_number}
الدولة: {country}
الشبكة: {carrier}
صحة الخط: {"✅ صالح" if valid else "❌ غير صالح"}

نتائج الاستخبارات:
- واتساب: {"✅ موجود" if whatsapp_active else "❌ غير موجود"}
- فيسبوك: {"✅ موجود" if facebook_exists else "❌ غير موجود"}
- إنستجرام: {"✅ موجود" if instagram_exists else "❌ غير موجود"}
- لينكدإن: {"✅ موجود" if linkedin_exists else "❌ غير موجود"}

تحليل خطورة الهدف: {secret_tag}

تحقيقات إضافية سرية:
- بريد ياهو المتوقع: {yahoo_email}
- بريد مسرب محتمل: {leaked_email if leaked_email else "❌ لا يوجد"}

- صنع بعقلية استخباراتية يمنية - BlackBox V4
"""
    bot.send_message(message.chat.id, report)

bot.remove_webhook()
bot.infinity_polling()