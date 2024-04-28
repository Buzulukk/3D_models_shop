import command
import main


def reduce_command(chat_id, active_command):
    main.effects_handler(chat_id, main.main_state.reduce(active_command.transform()))


def response_handler(response):
    match response["message"]["text"]:
        case "/start":
            start_handler(response)


def start_handler(response):
    chat_id = response["message"]["chat"]["id"]
    reduce_command(chat_id, command.Command(chat_id, command.Start()))
