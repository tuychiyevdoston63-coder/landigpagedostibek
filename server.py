import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

# .env faylini yuklaymiz
load_dotenv()

# static_folder-ni bo'sh qoldiramiz va static_url_path-ni ildizga yo'naltiramiz
app = Flask(__name__, static_folder=None)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route('/')
def index():
    # index.html ni joriy papkadan o'qib qaytaradi
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    # css/, js/ kabi istalgan papkadagi fayllarni to'g'ri yetkazib beradi
    return send_from_directory('.', filename)

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json() or {}
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({"success": False, "message": "Barcha maydonlarni to'ldiring!"}), 400

    telegram_message = (
        "━━━━━━━━━━━━━━━━━━\n"
        "📩 YANGI ARIZA\n\n"
        f"👤 Ism:\n{name}\n\n"
        f"📧 Email:\n{email}\n\n"
        f"💬 Xabar:\n{message}\n\n"
        "🌐 DOSTECH Landing Page\n"
        "━━━━━━━━━━━━━━━━━━"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": telegram_message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        res_data = response.json()
        
        if response.status_code == 200 and res_data.get("ok"):
            return jsonify({"success": True, "message": "Xabaringiz muvaffaqiyatli yuborildi."})
        else:
            return jsonify({"success": False, "message": "Telegram API xatoligi."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
