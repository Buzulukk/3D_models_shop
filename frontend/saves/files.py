import os

import requests

import command
import main
from materials_files.material import MaterialPhotos, MaterialDrawings, MaterialCloseups


def save_file(bot_token, tg_message):
    user_id = tg_message["message"]["chat"]["id"]
    order_id = main.main_state.users[user_id].active_order

    file_name = tg_message["message"]["document"]["file_name"]

    material_type = (main.main_state.users[user_id].orders[order_id]
                     .stage.body.materials.active_files_type)

    file_type_name = None
    match material_type:
        case MaterialPhotos():
            file_type_name = "photos"
        case MaterialDrawings():
            file_type_name = "drawings"
        case MaterialCloseups():
            file_type_name = "closeups"

    save_path = ("frontend/saves/saves/" + str(user_id) + "/" + str(order_id)
                 + "/files/" + file_type_name + "/" + file_name)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    request_link = "https://api.telegram.org/bot" + bot_token + "/getFile"
    file_data = requests.get(request_link, params={'file_id': tg_message["message"]["document"]["file_id"]}).json()
    file_path = file_data["result"]["file_path"]

    download_request_link = "https://api.telegram.org/file/bot" + bot_token + "/" + file_path
    response = requests.get(download_request_link)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
            main.main_state.reduce(
                command.Command(user_id, command.UploadFilesMarkSaved(order_id, material_type, file_name)).transform())
