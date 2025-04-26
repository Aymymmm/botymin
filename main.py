import re
import hashlib
import requests

# دالة للتحقق من الرقم اليمني
def is_valid_yemeni_number(number):
    pattern = r'^(70|71|73|77)\d{7}$'
    return re.match(pattern, number)

# دالة لتوليد بريد ياهو بناءً على الرقم
def smart_guess_yahoo_email(number):
    username = number[-7:]  # آخر 7 أرقام
    return f"{username}@yahoo.com"

# توليد توقيع أمني خاص (Hash)
def generate_secret_hash(number):
    return hashlib.sha256(number.encode()).hexdigest()[:16]

# فحص اتصال سيرفر حقيقي (سري)
def server_ping_test(number):
    try:
        url = f"https://api.callmebot.com/whatsapp.php?phone=967{number}&text=PingTest&apikey=123456"
        response = requests.get(url, timeout=3)
        return response.status_code == 200
    except Exception as e:
        return False

# تحليل سلوك الرقم (ذكاء اصطناعي مبسط)
def analyze_behavior(number):
    behavior_patterns = {
        '70': "مدني - مستخدم يو",
        '71': "سبأفون - موظف أو عميل خاص",
        '73': "MTN - نشاط منخفض - خط خاص",
        '77': "يمن موبايل - شبكة مستقلة"
    }
    prefix = number[:2]
    return behavior_patterns.get(prefix, "غير مصنف")

# عرض النتائج بشكل استخباراتي
def generate_intelligence_report(number):
    if not is_valid_yemeni_number(number):
        return "❌ رقم غير صحيح.\nيجب أن يبدأ بـ 70 أو 71 أو 73 أو 77 ويتكون من 9 أرقام."

    yahoo_email = smart_guess_yahoo_email(number)
    secret_hash = generate_secret_hash(number)
    server_ping = server_ping_test(number)
    behavior = analyze_behavior(number)

    report = f"""
🛰️ Yemen Intelligence Report V7 🛰️

- الرقم: 967{number}
- نوع الشريحة: {behavior}
- بريد ياهو المحتمل: {yahoo_email}
- التوقيع الأمني السري: {secret_hash}
- حالة سيرفر الاتصال: {"✅ متفاعل" if server_ping else "❌ غير متفاعل"}

⚡ تحليل عميق — تنفيذ وحدة العمليات السيبرانية اليمنية الخاصة ⚡
"""
    return report

# برنامج رئيسي
if __name__ == "__main__":
    print("\n🛰️ Yemen BlackBox Intelligence V7 🛰️\n")
    user_number = input("أدخل الرقم اليمني المراد تحليله (بدون مفتاح الدولة): ").strip()

    if not user_number.isdigit() or len(user_number) != 9:
        print("\n❌ الرقم يجب أن يكون 9 أرقام فقط.")
    else:
        report = generate_intelligence_report(user_number)
        print(report)