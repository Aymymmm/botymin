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
logging.basicConfig(level=logging.INFO)

# التوكن والـ API
BOT_TOKEN = '7756130100:AAEZAgI4mVZyjV2HulvNtBBZurKhVIDFd-8'
NUMVERIFY_API_KEY = '35aee4b59b91dad0fca3831889371f6e'

# تحقق من الرقم اليمني
def is_valid_yemeni_number(number: str) -> bool:
    if not re.fullmatch(r'(70|71|73|77)\d{7}', number):
        return False
    return True

# استعلام عن بيانات الرقم
async def lookup_number(phone_number: str):
    try:
        url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number=+967{phone_number}&country_code=YE"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        logging.error(f"خطأ في الاستعلام: {e}")
        return None

# توليد بريد ياهو عشوائي للرقم
def generate_fake_email(phone_number: str):
    prefix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
    return f"{prefix}{phone_number}@yahoo.com"

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك في Yemen BlackBox V2.\nأرسل رقم يمني يبدأ بـ (70,71,73,77) مكون من 9 أرقام للبحث.")

# عند استقبال رسالة
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if not text.isdigit():
        await update.message.reply_text("❌ أدخل رقم صحيح فقط.")
        return

    if not is_valid_yemeni_number(text):
        await update.message.reply_text("❌ رقم غير صحيح. يجب أن يكون رقم يمني صحيح مكون من 9 أرقام ويبدأ بـ (70,71,73,77).")
        return

    await update.message.reply_text("⏳ جاري البحث عن المعلومات...")

    info = await lookup_number(text)
    if info:
        result = f"🔍 النتائج:\n\n"
        result += f"✅ رقم صحيح: {info.get('valid')}\n"
        result += f"الدولة: {info.get('country_name')}\n"
        result += f"الشبكة: {info.get('carrier')}\n"
        result += f"الخط صالح: {info.get('line_type')}\n"
        result += f"البريد المتوقع: {generate_fake_email(text)}\n"
        result += f"آخر تحقق: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

        await update.message.reply_text(result)
    else:
        await update.message.reply_text("❌ فشل في جلب البيانات. حاول لاحقًا.")

# إعداد التطبيق
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()