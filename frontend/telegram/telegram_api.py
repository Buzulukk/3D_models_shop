import os

import uuid
import requests
from flask import request, jsonify, Flask, send_from_directory

import command
from frontend.saves.files import save_file
from main import effects_handler
from stateManager import main_state

BOT_TOKEN = '6947052492:AAECxz7hadze_qAJqiZpWEYVN-iivn8-4_Y'

app = Flask(__name__)


# example of getting some file
# http://localhost:8000/download/863600387/94bb87eb-3d4e-447c-8ded-395eb40e7d3d/files/photos/2xo2ka__01.jpg
@app.route('/download/<path:filename>')
def download_file(filename):
    directory = os.path.abspath(os.path.join(app.root_path, '../saves/saves'))
    print(directory)
    return send_from_directory(directory, filename, as_attachment=True)


# http://localhost:8000/approve?price=4200
@app.route('/approve', methods=['POST'])
def approve():
    data = request.get_json()

    user_id = data['user_id']
    order_id = uuid.UUID(data['order_id'])
    price = data['price']

    cmd = command.Command(user_id, command.GetInfoFromManager(order_id, price))
    effects = main_state.reduce(cmd.transform())
    effects_handler(cmd.user_id, effects)

    return jsonify(success=True)


@app.route('/telegram_webhooks_endpoint', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    print("Received data:", data)

    if "text" not in data["message"]:
        save_file(BOT_TOKEN, data)
    else:
        cmd = main_state.response(data)
        effects = main_state.reduce(cmd.transform())
        effects_handler(cmd.user_id, effects)

    return jsonify(success=True)


def send_message(chat_id, text):
    request_link = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
    }

    print(requests.post(request_link, data=data))


def send_message_with_buttons(chat_id, text, buttons):
    request_link = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": "{\"keyboard\":[" + ', '.join(f"[\"{item}\"]" for item in buttons)
                        + "],\"one_time_keyboard\":true,\"resize_keyboard\":true}"
    }

    print(requests.post(request_link, data=data))


def send_questionnaire_question(chat_id, questionnaire_question):
    request_link = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": questionnaire_question['message'],
        "reply_markup": "{\"keyboard\":[" + ', '.join(f"[\"{item}\"]" for item in questionnaire_question['buttons'])
                        + "],\"one_time_keyboard\":true,\"resize_keyboard\":true}"
    }

    print(requests.post(request_link, data=data))


app.run(port=8000, debug=True)
