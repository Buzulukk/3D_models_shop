import uuid
from dataclasses import dataclass

import state


class Start:
    pass


type Action = Start


def transform(self):
    match self.action:
        case Start():
            return state.CreateUser(self.user_id)


@dataclass
class Command:
    user_id: uuid.UUID
    action: Action

    def __init__(self, user_id: uuid.UUID, action: Action):
        self.user_id = user_id
        self.action = action

    transform = transform
