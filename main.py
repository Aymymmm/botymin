import telebot
import requests
from bs4 import BeautifulSoup
import json

API_TOKEN = '7756130100:AAEZAgI4mVZyjV2HulvNtBBZurKhVIDFd-8'
bot = telebot.TeleBotAPI_TOKEN = '35aee4b59b91dad0fca3831889371f6e,

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

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    number = message.text.strip()
    if number.startswith("+") or number.isdigit():
        bot.send_message(message.chat.id, "جاري البحث عن الرقم من عدة مصادر...")
        result_1 = search_emobiletracker(number)
        result_2 = search_freecarrierlookup(number)
        final_result = f"[emobiletracker]\n{result_1}\n\n[freecarrierlookup]\n{result_2}"
        bot.send_message(message.chat.id, final_result)
    else:
        bot.send_message(message.chat.id, "أرسل رقمًا يبدأ بـ + أو بدون رموز.")

bot.remove_webhook()
bot.infinity_polling()
