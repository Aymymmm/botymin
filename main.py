import telebot
import requests

API_TOKEN = "7756130100:AAEZAgI4mVZyjV2HulvNtBBZurKhVIDFd-8"
API_ACCESS_KEY = "35aee4b59b91dad0fca3831889371f6e"

bot = telebot.TeleBot(API_TOKEN)

# تخزين المحاولات
user_attempts = {}
allowed_code = "Yemen2025"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أدخل الرمز السري:")

@bot.message_handler(func=lambda message: True)
def check_code_or_number(message):
    user_id = message.from_user.id
    text = message.text.strip()

    # تحقق من اذا كان المستخدم أدخل رمز أو لا
    if user_id not in user_attempts:
        user_attempts[user_id] = {"tries": 0, "verified": False}

    # إذا المستخدم مش متحقق
    if not user_attempts[user_id]["verified"]:
        if text == allowed_code:
            user_attempts[user_id]["verified"] = True
            bot.reply_to(message, "تم التحقق! أرسل رقم الهاتف اليمني الذي تريد البحث عنه.")
        else:
            user_attempts[user_id]["tries"] += 1
            if user_attempts[user_id]["tries"] >= 5:
                bot.reply_to(message, "تم قفل حسابك بعد 5 محاولات فاشلة.")
            else:
                bot.reply_to(message, f"رمز خاطئ! حاول مرة أخرى. ({5 - user_attempts[user_id]['tries']} محاولة متبقية)")
        return

    # بعد التحقق، هنا نتحقق من الرقم
    if validate_yemeni_number(text):
        search_number_info(message, text)
    else:
        bot.reply_to(message, "أدخل رقمًا يمنيًا صحيحًا مكون من 9 أرقام أو مع مفتاح اليمن 967.")

def validate_yemeni_number(number):
    if number.isdigit():
        if len(number) == 9 and number.startswith(('7')):
            return True
        if len(number) == 12 and number.startswith('9677'):
            return True
    return False

def search_number_info(message, number):
    url = f"http://apilayer.net/api/validate?access_key={API_ACCESS_KEY}&number={number}&country_code=&format=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('valid'):
            info = f"معلومات الرقم:\n\n"
            info += f"الدولة: {data.get('country_name', 'غير معروف')}\n"
            info += f"شركة الاتصالات: {data.get('carrier', 'غير معروفة')}\n"
            info += f"الخط: {data.get('line_type', 'غير معروف')}\n"
            bot.reply_to(message, info)
        else:
            bot.reply_to(message, "الرقم غير صالح أو لا يوجد له بيانات.")
    else:
        bot.reply_to(message, "خطأ أثناء الاتصال بقاعدة البيانات. حاول لاحقًا.")

# حذف الويب هوك لو موجود + عمل بوت دائم
bot.remove_webhook()
bot.infinity_polling()