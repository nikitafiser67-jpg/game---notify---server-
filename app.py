from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Значения берутся из переменных окружения Railway
BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
CHAT_ID = os.environ.get('CHAT_ID', '5988591918')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        print(f"Ошибка отправки: {e}")

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    if data and 'name' in data:
        player_name = data['name']
        message = f"🎮 Игрок {player_name} зашёл в игру!"
        send_telegram_message(message)
        return jsonify({"ok": True}), 200
    return jsonify({"ok": False, "error": "Нет имени"}), 400

@app.route('/')
def index():
    return "Server is running!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
