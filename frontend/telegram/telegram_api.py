from flask import Flask, request, jsonify
import requests

import main

# from frontend.telegram.telegram_core import response_handler

app = Flask(__name__)

BOT_TOKEN = '6947052492:AAECxz7hadze_qAJqiZpWEYVN-iivn8-4_Y'


@app.route('/telegram_webhooks_endpoint', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    print("Received data:", data)

    command = main.main_state.response(data)
    effects = main.main_state.reduce(command.transform())
    main.effects_handler(command.user_id, effects)

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
        "reply_markup": "{\"keyboard\":[[" + ', '.join(f'"{item}"' for item in buttons)
                        + "]],\"one_time_keyboard\":true,\"resize_keyboard\":true}"
    }

    print(requests.post(request_link, data=data))


def send_questionnaire_question(chat_id, questionnaire_question):
    request_link = "https://api.telegram.org/bot" + BOT_TOKEN + "/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": questionnaire_question['message'],
        "reply_markup": "{\"keyboard\":[[" + ', '.join(f'"{item}"' for item in questionnaire_question['buttons'])
                        + "]],\"one_time_keyboard\":true,\"resize_keyboard\":true}"
    }

    print(requests.post(request_link, data=data))


app.run(port=8000, debug=True)
