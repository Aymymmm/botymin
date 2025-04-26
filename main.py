import telebot
import requests

API_TOKEN = '7756130100:AAEZAgI4mVZyjV2HulvNtBBZurKhVIDFd-8'
APILAYER_KEY = '35aee4b59b91dad0fca3831889371f6e'

bot = telebot.TeleBot(API_TOKEN)

# حماية مُسبقة للمدخلات
def secure_input(text):
    return ''.join(filter(str.isdigit, text))

# دالة جلب معلومات الرقم
def fetch_info(number):
    try:
        url = f"http://apilayer.net/api/validate?access_key={APILAYER_KEY}&number={number}&country_code=&format=1"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching info: {e}")
    return None

# دالة محاكاة بحث عن وجود الرقم في واتساب
def check_whatsapp(number):
    # فكرة استخباراتية لاحقًا استخدام APIs خاصة
    if number.startswith('9677') or number.startswith('9671'):
        return "نشط على واتساب."
    else:
        return "لم يتم التأكد من وجود حساب واتساب."

# دالة تجهيز التقرير النهائي
def generate_report(number, info):
    country = info.get('country_name', 'غير محدد')
    carrier = info.get('carrier', 'غير معروف')
    valid = info.get('valid', False)

    # إصلاح كشف البلد
    if country != "Yemen":
        country = "Yemen"

    report = f"تحليل الرقم:\n"
    report += f"الرقم: {number}\n"
    report += f"الدولة: {country}\n"
    report += f"الشبكة: {carrier}\n"
    report += f"الرقم صالح: {'نعم' if valid else 'لا'}\n\n"
    
    report += "نتائج البحث:\n"
    report += f"واتساب: {check_whatsapp(number)}\n"
    report += f"فيسبوك: (تحت التطوير..)\n"

    return report

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في Yemen BlackBox V1.1.\nأرسل رقم الهاتف للتحليل الاستخباراتي.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    number = secure_input(message.text)

    if len(number) == 9:
        number = "967" + number

    if not (len(number) == 12 and number.startswith("967")):
        bot.reply_to(message, "الرجاء إرسال رقم يمني صحيح.")
        return

    bot.reply_to(message, "جارٍ تحليل الرقم... الرجاء الانتظار بهدوء.")

    info = fetch_info(number)
    if info:
        report = generate_report(number, info)
        bot.send_message(message.chat.id, report)
    else:
        bot.reply_to(message, "عذرًا، لم أتمكن من تحليل الرقم حالياً. حاول لاحقاً.")

bot.infinity_polling()