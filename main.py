import telebot
import requests
import os

# استخدام متغيرات البيئة لحماية التوكن ومفتاح الAPI
API_TOKEN = os.getenv("API_TOKEN", "7756130100:AAEZAgI4mVZyjV2HulvNtBBZurKhVIDFd-8")
API_ACCESS_KEY = os.getenv("API_ACCESS_KEY", "35aee4b59b91dad0fca3831889371f6e")

bot = telebot.TeleBot(API_TOKEN)

# إدارة محاولات المستخدم
user_sessions = {}

# الرمز السري للدخول
SECRET_CODE = "Yemen2025"
MAX_TRIES = 5

def is_valid_yemeni_number(number: str) -> bool:
    """التحقق من صحة الرقم اليمني."""
    return (number.isdigit() and ((len(number) == 9 and number.startswith('7')) or (len(number) == 12 and number.startswith('9677'))))

def query_number_info(phone_number: str) -> dict:
    """طلب معلومات الرقم من API خارجي."""
    try:
        url = f"http://apilayer.net/api/validate?access_key={API_ACCESS_KEY}&number={phone_number}&country_code=&format=1"
        response = requests.get(url, timeout=10)
        if response.ok:
            return response.json()
        return None
    except Exception as e:
        print(f"Error querying API: {e}")
        return None

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user_sessions[user_id] = {"tries": 0, "verified": False}
    bot.reply_to(message, "مرحبًا بك.\nأدخل الرمز السري للمتابعة:")

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    user_id = message.from_user.id
    text = message.text.strip()

    # إعداد الجلسة للمستخدم إذا لم تكن موجودة
    if user_id not in user_sessions:
        user_sessions[user_id] = {"tries": 0, "verified": False}

    session = user_sessions[user_id]

    # التحقق من الرمز السري أولاً
    if not session["verified"]:
        if text == SECRET_CODE:
            session["verified"] = True
            bot.reply_to(message, "تم التحقق بنجاح.\nالآن أرسل رقم الهاتف اليمني.")
        else:
            session["tries"] += 1
            if session["tries"] >= MAX_TRIES:
                bot.reply_to(message, "لقد تجاوزت الحد الأقصى للمحاولات. أعد المحاولة لاحقًا.")
            else:
                tries_left = MAX_TRIES - session["tries"]
                bot.reply_to(message, f"رمز خاطئ! لديك {tries_left} محاولات متبقية.")
        return

    # بعد التحقق، التعامل مع أرقام الهواتف
    if is_valid_yemeni_number(text):
        bot.reply_to(message, "جاري البحث عن معلومات الرقم...")
        data = query_number_info(text)
        if data and data.get('valid', False):
            result_msg = (
                f"نتائج البحث:\n"
                f"الدولة: {data.get('country_name', 'غير معروفة')}\n"
                f"شركة الاتصال: {data.get('carrier', 'غير معروفة')}\n"
                f"نوع الخط: {data.get('line_type', 'غير معروف')}\n"
            )
            bot.reply_to(message, result_msg)
        else:
            bot.reply_to(message, "لم يتم العثور على معلومات لهذا الرقم.")
    else:
        bot.reply_to(message, "رقم غير صحيح.\nأدخل رقمًا صحيحًا (777xxxxxxx أو 967777xxxxxxx).")

# إزالة أي Webhook سابق لمنع الخطأ 409
bot.remove_webhook()

# بدء الاستماع للأوامر بدون توقف
bot.infinity_polling(timeout=10, long_polling_timeout=5)