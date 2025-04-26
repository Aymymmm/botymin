import logging
import re
import hashlib
import requests
import socket
import random
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# إعداد التسجيل
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# التوكن والـ API
BOT_TOKEN = '7756130100:AAEZAgI4mVZyjV2HulvNtBBZurKhVIDFd-8'
NUMVERIFY_API_KEY = '35aee4b59b91dad0fca3831889371f6e'

# تحقق من الرقم اليمني
def is_valid_yemeni_number(number: str) -> bool:
    return bool(re.fullmatch(r'(70|71|73|77)\d{7}', number))

# استعلام عن بيانات الرقم
async def lookup_number(phone_number: str):
    try:
        url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number=+967{phone_number}&country_code=YE"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        logging.error(f"خطأ في الاستعلام: {e}")
        return None

# توليد بريد ياهو عشوائي للرقم
def generate_fake_email(phone_number: str):
    prefix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
    return f"{prefix}{phone_number}@yahoo.com"

# توليد بصمة رقمية فريدة
def generate_fingerprint(phone_number: str):
    seed = phone_number + str(random.randint(1000, 9999))
    return hashlib.sha256(seed.encode()).hexdigest()[:16]

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا بك في Yemen BlackBox V3.\n"
        "أرسل رقم يمني (70,71,73,77) مكون من 9 أرقام لتحصل على معلوماته.\n"
        "كل عملية بحث آمنة وسرية."
    )

# عند استقبال رسالة
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("❌ أدخل أرقام فقط دون حروف.")
        return

    if not is_valid_yemeni_number(text):
        await update.message.reply_text("❌ رقم غير صحيح! تأكد أنه يبدأ بـ (70,71,73,77) ومكون من 9 أرقام.")
        return

    await update.message.reply_text("⏳ جاري تحليل الرقم...")

    info = await lookup_number(text)
    if info:
        carrier = info.get('carrier', 'غير معروف')
        valid = info.get('valid', False)
        line_type = info.get('line_type', 'غير محدد')

        result = (
            f"📄 النتيجة:\n\n"
            f"✅ صالح: {'نعم' if valid else 'لا'}\n"
            f"شركة الاتصالات: {carrier}\n"
            f"نوع الخط: {line_type}\n"
            f"📧 بريد وهمي: {generate_fake_email(text)}\n"
            f"🧬 بصمة رقم: {generate_fingerprint(text)}\n"
            f"⏰ وقت البحث: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        await update.message.reply_text(result)
    else:
        await update.message.reply_text("❌ تعذر جلب المعلومات. جرب لاحقًا.")

# إعداد التطبيق
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()