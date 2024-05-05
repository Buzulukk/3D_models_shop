import uuid
from dataclasses import dataclass
from typing import Any

import command
import user
import effect
from materials_files.materials import Materials
from materials_files.material import Material


class CreateUser:
    user_id: uuid.UUID

    def __init__(self, user_id: uuid.UUID):
        self.user_id = user_id


class User:
    user_id: uuid.UUID
    action: user.Action

    def __init__(self, user_id: uuid.UUID, action: user.Action):
        self.user_id = user_id
        self.action = action


class ViewFiles:
    user_id: uuid.UUID
    material: Material

    def __init__(self, user_id: uuid.UUID, material: Material):
        self.user_id = user_id
        self.material = material


type Action = CreateUser | User | ViewFiles


def reduce(self, action: Action):
    match action:
        case CreateUser(user_id=user_id):
            self.users[user_id] = user.User(user_id)
            return [
                effect.MessageWithButtons(
                    "Добрый день! Вы обратились в отдел разработки 3D моделей. Для того чтобы начать, нажмите на кнопку “Заказать модель” из меню.",
                    ["Заказать модель"]
                )
            ]
        case ViewFiles(user_id=user_id, material=material):
            materials_set = self.get_set(user_id, self.users[user_id].active_order)
            return self.view_files(user_id, self.users[user_id].active_order, material, materials_set)
        case User(user_id=user_id, action=action):
            return self.users[user_id].reduce(action)


def response(self, tg_message):
    user_id = tg_message["message"]["chat"]["id"]

    match tg_message["message"]["text"]:
        case "/start":
            return command.Command(user_id, command.Start())
        case _:
            return self.users[user_id].response(tg_message)


def view(self, user_id: uuid.UUID):
    return self.users[user_id].view()


def view_files(self, user_id: uuid.UUID, order_id: uuid.UUID, material: Materials, materials_set: Any):
    return self.users[user_id].view_files(order_id, material, materials_set)


def get_set(self, user_id: uuid.UUID, order_id: uuid.UUID):
    return self.users[user_id].get_set(order_id)


def ask_info_for_contract(self, user_id: uuid.UUID):
    return self.users[user_id].ask_info_for_contract()


@dataclass
class State:
    users: {uuid.UUID, user.User}

    def __init__(self):
        self.users = {}

    reduce = reduce
    view = view
    view_files = view_files
    get_set = get_set
    ask_info_for_contract = ask_info_for_contract
    response = response
