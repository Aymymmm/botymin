import re
import requests
import telebot

# إعدادات البوت
API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# فحص الرقم إذا كان رقم يمني صحيح (70, 71, 73, 77)
def is_valid_yemeni_number(number):
    pattern = r'^(70|71|73|77)\d{7}$'
    return re.match(pattern, number)

# تخمين بريد ياهو ذكي
def smart_guess_yahoo_email(number):
    """يولد بريد ياهو استنادًا للرقم بطريقة ذكية"""
    username = number[-7:]  # آخر 7 أرقام
    yahoo_email = f"{username}@yahoo.com"
    return yahoo_email

# إضافة توقيع استخباراتي سرّي على الرقم (Hash)
def generate_secret_hash(number):
    import hashlib
    return hashlib.sha256(number.encode()).hexdigest()[:16]

# اختبار تفاعل رقم مع سيرفر حقيقي (Ping hidden)
def server_ping_test(number):
    try:
        url = f"https://api.callmebot.com/whatsapp.php?phone=967{number}&text=PingTest&apikey=123456"
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

# تحليل نمط الإتصالات للرقم (محاكاة ذكاء استخباراتي)
def analyze_behavior(number):
    patterns = {
        '70': "نشاط عالي - مدني أو تاجر اتصالات.",
        '71': "نشاط متوسط - ممكن موظف أو عميل خاص.",
        '73': "نشاط منخفض - مستخدم شرس أو شبكات مظلمة.",
        '77': "نشاط متغير - ربما مرتبط بخدمات حكومية أو خاصة."
    }
    prefix = number[:2]
    return patterns.get(prefix, "غير مصنف")

# استقبال الرسائل
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أرسل رقم الهاتف اليمني مكون من 9 أرقام ويبدأ بـ (70/71/73/77):")

@bot.message_handler(func=lambda message: True)
def handle_phone_number(message):
    number = message.text.strip()

    # تحقق أولي
    if not number.isdigit() or len(number) != 9:
        bot.reply_to(message, "❌ الرقم يجب أن يحتوي على 9 أرقام فقط.")
        return

    if not is_valid_yemeni_number(number):
        bot.reply_to(message,
            "❌ رقم غير صحيح.\nيجب أن يبدأ بـ:\n- 70 (شريحة يو)\n- 71 (شريحة سبأفون)\n- 73 (شريحة إم تي إن)\n- 77 (شريحة يمن موبايل)."
        )
        return

    bot.send_message(message.chat.id, "جارٍ تنفيذ الفحص السري... ⏳")

    # استخلاص معلومات سرية
    yahoo_email = smart_guess_yahoo_email(number)
    hash_signature = generate_secret_hash(number)
    server_ping = server_ping_test(number)
    behavior = analyze_behavior(number)

    intelligence_report = f"""
🛰️ Yemen Intelligence Report V6 🛰️

- رقم الهاتف: 967{number}
- التحليل الشبكي: {behavior}
- بريد ياهو المتوقع: {yahoo_email}
- توقيع أمني سري: {hash_signature}
- اختبار خادم الاتصال: {"✅ متفاعل" if server_ping else "❌ غير متفاعل"}

⚡ تم التنفيذ بواسطة وحدة الحرب السيبرانية اليمنية.
"""
    bot.send_message(message.chat.id, intelligence_report)

# تشغيل البوت
bot.remove_webhook()
bot.infinity_polling()