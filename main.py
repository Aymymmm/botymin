import logging
import re
import requests
import hashlib
import socket
import random
import phonenumbers
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# تسجيل اللوغ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# بيانات البوت
BOT_TOKEN = '7756130100:AAEZAgI4mVZyjV2HulvNtBBZurKhVIDFd-8'
API_KEY = '35aee4b59b91dad0fca3831889371f6e'

# دالة التحقق من الرقم اليمني
def is_valid_yemeni_number(number: str) -> bool:
    if not number.isdigit() or len(number) != 9:
        return False
    prefixes = ("70", "71", "73", "77")
    return number.startswith(prefixes)

# تحليل أمني للرقم عبر API وهمي
def deep_intelligence_analysis(number: str) -> str:
    hash_value = hashlib.sha256(number.encode()).hexdigest()
    try:
        response = requests.get(f'https://api.apilayer.com/number_verification/validate?number={number}', 
                                 headers={'apikey': API_KEY})
        if response.status_code == 200:
            data = response.json()
            carrier = data.get("carrier", "مجهول")
            location = data.get("location", "غير معروف")
            return f"تحليل ذكي:\n- الشركة: {carrier}\n- الموقع: {location}\n- البصمة: {hash_value[:12]}"
        else:
            return "فشل الاتصال بالـ API."
    except Exception as e:
        return f"خطأ أثناء التحليل: {e}"

# رسالة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('أرسل لي رقم هاتف يمني مكون من 9 أرقام، وسأكشف لك البريد والمعلومات الخفية.')

# التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if is_valid_yemeni_number(text):
        intel_result = deep_intelligence_analysis(text)
        await update.message.reply_text(f"✅ رقم صحيح.\n{intel_result}")
    else:
        await update.message.reply_text("❌ رقم غير صحيح. يجب أن يكون رقم يمني صحيح مكون من 9 أرقام ويبدأ بـ (70/71/73/77).")

# إعداد البوت
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())