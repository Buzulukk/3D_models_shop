import uuid
from dataclasses import dataclass

import user


class CreateUser:
    user_id: uuid.UUID

    def __init__(self, user_id: uuid.UUID):
        self.user_id = user_id


class User:
    user_id: uuid.UUID
    action: user.Action


type Action = CreateUser | User


def reduce(self, action: Action):
    match action:
        case CreateUser(user_id=user_id):
            self.users[user_id] = user.User(user_id)
        case User(user_id=user_id):
            self.users[user_id].reduce(action)


@dataclass
class State:
    users: {uuid.UUID, user.User}

    def __init__(self):
        self.users = {}

    reduce = reduce
