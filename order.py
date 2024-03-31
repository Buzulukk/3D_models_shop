import uuid
from dataclasses import dataclass

import effect
import order_materials


class SetOrderName:
    order_name: str

    def __init__(self, order_name: str):
        self.order_name = order_name


class Questionnaire:
    answer: str

    def __init__(self, answer: str):
        self.answer = answer


type Action = SetOrderName | Questionnaire


def reduce(self, action: Action):
    match action:
        case SetOrderName(order_name=order_name):
            self.order_name = order_name
            return [
                effect.Nothing()
            ]
        case Questionnaire(answer=answer):
            return self.order_materials.reduce(answer)


@dataclass
class Order:
    order_id: uuid.UUID
    order_name: str
    order_materials: order_materials.OrderMaterials

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id
        self.order_name = ""
        self.order_materials = order_materials.OrderMaterials(None, None, None)

    reduce = reduce
