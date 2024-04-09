import uuid
from dataclasses import dataclass
import user
import effect


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


type Action = CreateUser | User


def reduce(self, action: Action):
    match action:
        case CreateUser(user_id=user_id):
            self.users[user_id] = user.User(user_id)
            return [
                effect.Message(
                    "Добрый день! Вы обратились в отдел разработки 3D моделей. Для того чтобы начать, нажмите на кнопку “Заказать модель” из меню.")
            ]
        case User(user_id=user_id, action=action):
            return self.users[user_id].reduce(action)


def view(self, user_id: uuid.UUID, order_id: uuid.UUID):
    return self.users[user_id].view(order_id)


@dataclass
class State:
    users: {uuid.UUID, user.User}

    def __init__(self):
        self.users = {}

    reduce = reduce
    view = view
