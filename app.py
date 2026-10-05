from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# ================= НАСТРОЙКИ =================
BOT_TOKEN = '8843037227:AAGw4eVEoZCSGnCfpC67SCk2z9G9uEwJLzk'
CHANNEL_LINK = 'https://t.me/OxideDropchik'
CHANNEL_NAME = 'Oxide Drop'
CHAT_ID = '5988591918'

# ================= ОТПРАВКА СООБЩЕНИЙ =================
def send_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Ошибка: {e}")

# ================= ПРИВЕТСТВИЕ =================
def send_welcome(chat_id):
    message = (
        f"👋 <b>Привет!</b>\n\n"
        f"📢 Подпишись на наш канал:\n"
        f"<b>{CHANNEL_NAME}</b>\n\n"
        f"👇 Жми кнопку ниже!"
    )
    reply_markup = {
        "inline_keyboard": [
            [{"text": "📢 Перейти в канал", "url": CHANNEL_LINK}]
        ]
    }
    send_message(chat_id, message, reply_markup)

# ================= WEBHOOK ДЛЯ TELEGRAM =================
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data or 'message' not in data:
        return 'ok', 200

    message = data['message']
    chat_id = message['chat']['id']
    text = message.get('text', '')

    if text == '/start':
        send_welcome(chat_id)

    return 'ok', 200

# ================= УВЕДОМЛЕНИЕ О ВХОДЕ В ИГРУ =================
@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    if data and 'name' in data:
        player_name = data['name']
        message = f"🎮 Игрок {player_name} зашёл в игру!"
        send_message(CHAT_ID, message)
        return jsonify({"ok": True}), 200
    return jsonify({"ok": False}), 400

@app.route('/')
def index():
    return "Server is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
