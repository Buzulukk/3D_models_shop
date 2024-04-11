import uuid
from dataclasses import dataclass
from typing import Any

import order
import effect
from materials_files.materials import Materials


class CreateOrder:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


class RemoveOrder:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


class Order:
    order_id: uuid.UUID
    action: order.Action

    def __init__(self, order_in: uuid.UUID, action: order.Action):
        self.order_id = order_in
        self.action = action


type Action = CreateOrder | RemoveOrder | Order


def reduce(self, action: Action):
    match action:
        case CreateOrder(order_id=order_id):
            self.orders[order_id] = order.Order(order_id)
            return [
                effect.Message("Пожалуйста, введите название вашего товара: ")
            ]
        case RemoveOrder(order_id=order_id):
            del self.orders[order_id]
            return [
                effect.Message("Заказ удален")
            ]
        case Order(order_id=order_id, action=action):
            return self.orders[order_id].reduce(action)


def view(self, order_id: uuid.UUID):
    return self.orders[order_id].view()


def view_files(self, order_id: uuid.UUID, material: Materials, materials_set: Any):
    return self.orders[order_id].view_files(material, materials_set)


def get_set(self, order_id: uuid.UUID):
    return self.orders[order_id].get_set()


@dataclass
class User:
    user_id: uuid.UUID
    orders: {uuid.UUID, order.Order}

    def __init__(self, user_id: uuid.UUID):
        self.user_id = user_id
        self.orders = {}

    reduce = reduce
    view = view
    view_files = view_files
    get_set = get_set
