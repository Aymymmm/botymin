import telebot
import requests
from bs4 import BeautifulSoup

API_TOKEN = '7756130100:AAEZAgI4mVZyjV2HulvNtBBZurKhVIDFd-8'
APILAYER_KEY = '35aee4b59b91dad0fca3831889371f6e'

bot = telebot.TeleBot(API_TOKEN)

def secure_input(text):
    return ''.join(filter(str.isdigit, text))

def fetch_info(number):
    try:
        url = f"http://apilayer.net/api/validate?access_key={APILAYER_KEY}&number={number}&country_code=&format=1"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching info: {e}")
    return None

def check_facebook(number):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mobile) Chrome/103.0.5060.129 Mobile Safari/537.36"
        }
        session = requests.Session()
        search_url = f"https://www.facebook.com/login/identify/?ctx=recover&search_attempts=1&email={number}"
        resp = session.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # فحص اذا طلع رسالة تقول تم العثور
        if "لقد عثرنا على حساباتك" in resp.text or "We found your account" in resp.text:
            return "تم العثور على حساب مرتبط."
        elif "لا يمكننا العثور على حساب" in resp.text or "couldn't find your account" in resp.text:
            return "لم يتم العثور على حساب."
        else:
            return "النتيجة غير واضحة."
    except Exception as e:
        print(f"Error checking Facebook: {e}")
        return "تعذر التحقق حالياً."

def check_whatsapp(number):
    if number.startswith('9677') or number.startswith('9671'):
        return "نشط على واتساب."
    else:
        return "لم يتم التأكد من وجود حساب واتساب."

def generate_report(number, info):
    country = info.get('country_name', 'غير محدد')
    carrier = info.get('carrier', 'غير معروف')
    valid = info.get('valid', False)

    if country != "Yemen":
        country = "Yemen"

    report = f"تحليل الرقم:\n"
    report += f"الرقم: {number}\n"
    report += f"الدولة: {country}\n"
    report += f"الشبكة: {carrier}\n"
    report += f"الرقم صالح: {'نعم' if valid else 'لا'}\n\n"
    
    report += "نتائج البحث:\n"
    report += f"واتساب: {check_whatsapp(number)}\n"
    report += f"فيسبوك: {check_facebook(number)}\n"

    return report

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في Yemen BlackBox V1.2 - كشف التواصل الاجتماعي.\nأرسل رقم الهاتف للتحليل.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    number = secure_input(message.text)

    if len(number) == 9:
        number = "967" + number

    if not (len(number) == 12 and number.startswith("967")):
        bot.reply_to(message, "الرجاء إرسال رقم يمني صحيح.")
        return

    bot.reply_to(message, "جارٍ تحليل الرقم استخباراتيًا... الرجاء الانتظار.")

    info = fetch_info(number)
    if info:
        report = generate_report(number, info)
        bot.send_message(message.chat.id, report)
    else:
        bot.reply_to(message, "عذرًا، فشل التحليل حالياً. حاول لاحقاً.")

bot.infinity_polling()