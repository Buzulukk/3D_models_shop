import uuid
from dataclasses import dataclass

import effect

from materials_files import materials, photos


class SetOrderName:
    order_name: str

    def __init__(self, order_name: str):
        self.order_name = order_name


class Materials:
    action: materials.Action

    def __init__(self, action: materials.Action):
        self.action = action


type Action = SetOrderName | Materials


def reduce(self, action: Action):
    match action:
        case SetOrderName(order_name=order_name):
            self.order_name = order_name
            return [
                effect.Nothing()
            ]
        case Materials(action=action):
            return self.materials.reduce(action)


@dataclass
class Order:
    order_id: uuid.UUID
    order_name: str
    materials: materials.Materials

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id
        self.order_name = ""
        self.materials = materials.Materials(photos.PhotosUnknown())

    reduce = reduce
