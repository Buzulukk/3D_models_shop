import uuid
from dataclasses import dataclass

import order
import state
import user


class Start:
    pass


class CreateOrder:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


class SetOrderName:
    order_id: uuid.UUID
    order_name: str

    def __init__(self, order_id: uuid.UUID, order_name: str):
        self.order_id = order_id
        self.order_name = order_name


class Questionnaire:
    order_id: uuid.UUID
    answer: str

    def __init__(self, order_id: uuid.UUID, answer: str):
        self.order_id = order_id
        self.answer = answer


type Action = Start | CreateOrder | SetOrderName | Questionnaire


def transform(self):
    match self.action:
        case Start():
            return state.CreateUser(self.user_id)
        case CreateOrder(order_id=order_id):
            return state.User(self.user_id, user.CreateOrder(order_id))
        case SetOrderName(order_id=order_id, order_name=order_name):
            return state.User(self.user_id, user.Order(order_id, order.SetOrderName(order_name)))
        case Questionnaire(order_id=order_id, answer=answer):
            return state.User(self.user_id, user.Order(order_id, order.Questionnaire(answer)))


@dataclass
class Command:
    user_id: uuid.UUID
    action: Action

    def __init__(self, user_id: uuid.UUID, action: Action):
        self.user_id = user_id
        self.action = action

    transform = transform
