import uuid
from dataclasses import dataclass

import order


class CreateOrder:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


class RemoveOrder:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


type Action = CreateOrder | RemoveOrder


def reduce(self, action: Action):
    match action:
        case CreateOrder(order_id):
            self.orders[order_id] = order.Order(order_id)
        case RemoveOrder(order_id):
            del self.orders[order_id]


@dataclass
class User:
    user_id: uuid.UUID
    orders: {uuid.UUID, order.Order}

    def __init__(self, user_id: uuid.UUID):
        self.user_id = user_id
        self.orders = {}

    reduce = reduce
