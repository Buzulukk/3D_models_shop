import os

import requests

from stateManager import main_state


def send_info_to_manager(user_id):
    order_id = main_state.users[user_id].active_order

    photos_links = []
    photos_path = "frontend/saves/saves/" + str(user_id) + "/" + str(order_id) + "/files/photos"
    for file in os.listdir(photos_path):
        photos_links.append(os.path.join(photos_path, file)[21:])
    drawings_links = []
    drawings_path = "frontend/saves/saves/" + str(user_id) + "/" + str(order_id) + "/files/drawings"
    for file in os.listdir(drawings_path):
        drawings_links.append(os.path.join(drawings_path, file)[21:])
    closeups_links = []
    closeups_path = "frontend/saves/saves/" + str(user_id) + "/" + str(order_id) + "/files/closeups"
    for file in os.listdir(closeups_path):
        closeups_links.append(os.path.join(closeups_path, file)[21:])

    data = {
        "chat_id": user_id,
        "user_name": main_state.users[user_id].user_name,
        "order_id": str(order_id),
        "order_name": main_state.users[user_id].orders[order_id].stage.base.name,
        "file_links": {
            "photos": photos_links,
            "drawings": drawings_links,
            "closeups": closeups_links
        }
    }

    request_link = "http://localhost:1234"

    print(requests.post(request_link, json=data))
