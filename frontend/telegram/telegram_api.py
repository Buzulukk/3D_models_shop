from flask import Flask, request, jsonify
import requests

from frontend.telegram.telegram_core import response_handler

app = Flask(__name__)

BOT_TOKEN = '6947052492:AAECxz7hadze_qAJqiZpWEYVN-iivn8-4_Y'


@app.route('/telegram_webhooks_endpoint', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    print("Received data:", data)

    response_handler(data)

    return jsonify(success=True)


def send_message(chat_id, text):
    request_link = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
    }

    print(requests.post(request_link, data=data))


app.run(port=8000, debug=True)
