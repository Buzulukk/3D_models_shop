import requests


def send_info_to_manager():
    request_link = "http://localhost:1234"
    data = {
        "info": "some_text"
    }

    print(requests.post(request_link, json=data))
