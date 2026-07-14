import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

# .env faylini yuklaymiz
load_dotenv()

# 'static' papkasini Flask uchun belgilaymiz
app = Flask(__name__, static_folder='static')

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route('/')
def index():
    # Asosiy sahifani qaytaradi
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    # static papkasi ichidagi barcha fayllarni (css, js) xatosiz uzatadi
    return send_from_directory('static', filename)

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
        f"👤 Ism: {name}\n"
        f"📧 Email: {email}\n"
        f"💬 Xabar: {message}\n\n"
        "🌐 DOSTECH Landing Page\n"
        "━━━━━━━━━━━━━━━━━━"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": telegram_message, "parse_mode": "HTML"}

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return jsonify({"success": True, "message": "✅ Xabaringiz yuborildi."})
        return jsonify({"success": False, "message": "❌ Xatolik yuz berdi."}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
