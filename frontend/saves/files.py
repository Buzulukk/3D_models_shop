import os

import requests

import main
from materials_files.material import MaterialPhotos, MaterialDrawings, MaterialCloseups


def save_file(bot_token, tg_message):
    user_id = tg_message["message"]["chat"]["id"]

    file_type = (main.main_state.users[user_id].orders[main.main_state.users[user_id].active_order]
                 .stage.body.materials.active_files_type)

    match file_type:
        case MaterialPhotos():
            file_type = "photos"
        case MaterialDrawings():
            file_type = "drawings"
        case MaterialCloseups():
            file_type = "closeups"

    save_path = ("frontend/saves/saves/" + str(user_id) + "/" + str(main.main_state.users[user_id].active_order)
                 + "/files/" + file_type + "/" + tg_message["message"]["document"]["file_name"])
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    request_link = "https://api.telegram.org/bot" + bot_token + "/getFile"
    file_data = requests.get(request_link, params={'file_id': tg_message["message"]["document"]["file_id"]}).json()
    file_path = file_data["result"]["file_path"]

    download_request_link = "https://api.telegram.org/file/bot" + bot_token + "/" + file_path
    response = requests.get(download_request_link)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
