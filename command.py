import uuid
from dataclasses import dataclass
from typing import Any

from materials_files import materials
from materials_files.material import Material
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


class QuestionnaireAsk:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


class QuestionnaireAnswer:
    order_id: uuid.UUID
    response: Any

    def __init__(self, order_id: uuid.UUID, response: Any):
        self.order_id = order_id
        self.response = response


class QuestionnaireCheck:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


class UploadFilesAsk:
    order_id: uuid.UUID
    material: Material

    def __init__(self, order_id: uuid.UUID, material: Material):
        self.order_id = order_id
        self.material = material


class UploadFilesMarkSaved:
    order_id: uuid.UUID
    material: Material

    def __init__(self, order_id: uuid.UUID, material: Material):
        self.order_id = order_id
        self.material = material


class SendInfoToManager:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


type Action = (Start | CreateOrder | SetOrderName | QuestionnaireAsk | QuestionnaireAnswer | QuestionnaireCheck |
               UploadFilesAsk | UploadFilesMarkSaved | SendInfoToManager)


def transform(self):
    match self.action:
        case Start():
            return state.CreateUser(self.user_id)
        case CreateOrder(order_id=order_id):
            return state.User(self.user_id, user.CreateOrder(order_id))
        case SetOrderName(order_id=order_id, order_name=order_name):
            return state.User(self.user_id, user.Order(order_id, order.SetOrderName(order_name)))
        case QuestionnaireAsk(order_id=order_id):
            return state.User(self.user_id, user.Order(order_id, order.Materials(materials.View())))
        case QuestionnaireAnswer(order_id=order_id, response=response):
            return state.User(self.user_id, user.Order(order_id, order.Materials(materials.Change(response))))
        case QuestionnaireCheck(order_id=order_id):
            return state.User(self.user_id, user.Order(order_id, order.Materials(materials.GetSet())))
        case UploadFilesAsk(order_id=order_id, material=material):
            return state.User(self.user_id, user.Order(order_id, order.Materials(materials.UploadFilesAsk(material))))
        case UploadFilesMarkSaved(order_id=order_id, material=material):
            return state.User(self.user_id,
                              user.Order(order_id, order.Materials(materials.UploadFilesMarkSaved(material))))
        case SendInfoToManager(order_id=order_id):
            return state.User(self.user_id, user.Order(order_id, order.SendInfoToManager()))


@dataclass
class Command:
    user_id: uuid.UUID
    action: Action

    def __init__(self, user_id: uuid.UUID, action: Action):
        self.user_id = user_id
        self.action = action

    transform = transform
