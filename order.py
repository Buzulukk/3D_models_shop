import uuid
from dataclasses import dataclass

import effect


class SetOrderName:
    order_name: str

    def __init__(self, order_name: str):
        self.order_name = order_name


type Action = SetOrderName


def reduce(self, action: Action):
    match action:
        case SetOrderName(order_name=order_name):
            self.order_name = order_name
            return [
                effect.Nothing()
            ]


@dataclass
class Order:
    order_id: uuid.UUID
    order_name: str

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id
        self.order_name = ""

    reduce = reduce
