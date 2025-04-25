import telebot
import requests
from bs4 import BeautifulSoup
import json

# توكن البوت
API_TOKEN = '7756130100:AAEZAgI4mVZyjV2HulvNtBBZurKhVIDFd-8'
bot = telebot.TeleBot(API_TOKEN)

# دالة للبحث في emobiletracker
def search_emobiletracker(number):
    try:
        url = f"https://www.emobiletracker.com/track/?phone={number}&submit=Track"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.find("table", class_="tracking-table")
        if table:
            rows = table.find_all("tr")
            info = []
            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True)
                    val = cols[1].get_text(strip=True)
                    info.append(f"{key}: {val}")
            return "\n".join(info)
        else:
            return "لا توجد بيانات واضحة من emobiletracker."
    except Exception as e:
        return f"خطأ في emobiletracker: {str(e)}"

# دالة للبحث في freecarrierlookup
def search_freecarrierlookup(number):
    try:
        url = f"https://freecarrierlookup.com/getcarrier.php?phonenumber={number}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200 and res.text.strip().startswith("{"):
            data = json.loads(res.text)
            return f"مزود الخدمة: {data.get('carrier')}\nالنوع: {data.get('type')}"
        else:
            return "لا توجد نتائج صالحة من freecarrierlookup."
    except Exception as e:
        return f"خطأ في freecarrierlookup: {str(e)}"

# دالة لاستخدام الـ API الجديدة
def use_new_api(number):
    try:
        # هنا يتم استخدام الـ API الجديدة
        url = f"https://api.example.com/v1/lookup?phone={number}&api_key=35aee4b59b91dad0fca3831889371f6e"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        
        if res.status_code == 200:
            data = res.json()  # استجابة JSON من الـ API
            return f"النتائج: {data.get('result')}"
        else:
            return "لا توجد نتائج صالحة من الـ API الجديدة."
    except Exception as e:
        return f"خطأ في استخدام الـ API الجديدة: {str(e)}"

# التعامل مع الرسائل في البوت
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    number = message.text.strip()
    if number.startswith("+") or number.isdigit():
        bot.send_message(message.chat.id, "جاري البحث عن الرقم من عدة مصادر...")
        
        # استخدام جميع APIs
        result_1 = search_emobiletracker(number)
        result_2 = search_freecarrierlookup(number)
        result_3 = use_new_api(number)  # استخدام الـ API الجديدة
        
        final_result = f"[emobiletracker]\n{result_1}\n\n[freecarrierlookup]\n{result_2}\n\n[API الجديدة]\n{result_3}"
        
        bot.send_message(message.chat.id, final_result)
    else:
        bot.send_message(message.chat.id, "أرسل رقمًا يبدأ بـ + أو بدون رموز.")

# بدء البوت وتشغيله
bot.remove_webhook()
bot.infinity_polling()
