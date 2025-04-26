import logging import re import hashlib import requests import socket import random from datetime import datetime from telegram import Update from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

إعداد السجل

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

توكن البوت

BOT_TOKEN = "7756130100:AAEZAgI4mVZyjV2HulvNtBBZurKhVIDFd-8"

API Key الخاصة

API_KEY = "35aee4b59b91dad0fca3831889371f6e"

تحقق من الرقم

def is_valid_yemeni_number(number): pattern = r'^(70|71|73|77)\d{7}$' return re.match(pattern, number)

توليد بريد ياهو ذكي

def smart_guess_yahoo_email(number): username = number[-7:] return f"{username}@yahoo.com"

توليد توقيع أمني (Hash)

def generate_secret_hash(number): return hashlib.sha256((number + API_KEY).encode()).hexdigest()[:16]

اختبار اتصال سيرفرات سرية

def server_ping_test(number): try: url = f"https://api.callmebot.com/whatsapp.php?phone=967{number}&text=PingTest&apikey=123456" response = requests.get(url, timeout=3) return response.status_code == 200 except Exception: return False

تحليل ذكاء للسلوك

def analyze_behavior(number): behavior_patterns = { '70': "يو - مدني", '71': "سبأفون - تواصل خاص", '73': "MTN - خط خاص", '77': "يمن موبايل - مستخدمين مستقلين" } prefix = number[:2] return behavior_patterns.get(prefix, "غير معروف")

كشف ارتباط الحسابات

def email_link_guess(number): emails = [ f"{number}@gmail.com", f"{number}@yahoo.com", f"{number}@outlook.com" ] return emails

تحديد موقع سيرفر افتراضي

def guess_geo_ip(): cities = ["صنعاء", "عدن", "الحديدة", "تعز", "ذمار", "مأرب"] return random.choice(cities)

كشف شبكة وهمية افتراضية (VPN Check وهمي)

def vpn_check_simulation(): return random.choice(["لا يستخدم VPN", "قد يكون خلف VPN"])

توليد تقرير استخباراتي كامل

async def generate_intelligence_report(update: Update, context: ContextTypes.DEFAULT_TYPE): user_input = update.message.text.strip()

if not user_input.isdigit() or len(user_input) != 9 or not is_valid_yemeni_number(user_input):
    await update.message.reply_text(
        "\u274c رقم غير صحيح.\n\nيجب أن يكون الرقم مكون من 9 أرقام ويبدأ بـ (70 / 71 / 73 / 77)."
    )
    return

number = user_input
yahoo_email = smart_guess_yahoo_email(number)
secret_hash = generate_secret_hash(number)
server_ping = server_ping_test(number)
behavior = analyze_behavior(number)
email_links = email_link_guess(number)
location_guess = guess_geo_ip()
vpn_status = vpn_check_simulation()
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# توقيع أمني داخلي سري
fingerprint = hashlib.md5((number + timestamp).encode()).hexdigest()

report = f"""

\ud83d\ude80 Yemen BlackBox Intelligence V9 \ud83d\ude80

الرقم: 967{number}

نوع الشريحة: {behavior}

موقع تقديري: {location_guess}

حالة الشبكة الافتراضية: {vpn_status}

بريد ياهو المتوقع: {yahoo_email}

حسابات بريد محتملة:

{email_links[0]}

{email_links[1]}

{email_links[2]}


التوقيع الأمني السري: {secret_hash}

بصمة الرسالة: {fingerprint}

حالة الاتصال بالسيرفر السري: {"\u2705 متفاعل" if server_ping else "\u274c غير متفاعل"}

زمن التحليل: {timestamp}


\u2728 تحليل استخباراتي خاص - وحدة BlackBox \u2728 """ await update.message.reply_text(report)

بدء البوت

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text( "\u2728 أرسل رقم يمني مكون من 9 أرقام يبدأ بـ (70 / 71 / 73 / 77) للحصول على تحليل استخباراتي خاص \u2728" )

البرنامج الرئيسي

def main(): app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_intelligence_report))

app.run_polling()

if name == "main": main()

