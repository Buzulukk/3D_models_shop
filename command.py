import datetime
import uuid
from dataclasses import dataclass
from typing import Any

import contractInfo
from materials_files import materials
from materials_files.material import Material
import order
import state
import user
from stages import stageBase, stageQuest, stageMatter, stageContract, stageFinal


class Start:
    pass


class CreateOrder:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


class RemoveOrder:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


class SetOrderName:
    order_id: uuid.UUID
    order_name: str

    def __init__(self, order_id: uuid.UUID, order_name: str):
        self.order_id = order_id
        self.order_name = order_name


class QuestionnaireAnswer:
    order_id: uuid.UUID
    response: Any

    def __init__(self, order_id: uuid.UUID, response: Any):
        self.order_id = order_id
        self.response = response


class RestartQuestionnaire:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


class ViewFiles:
    material: Material

    def __init__(self, material: Material):
        self.material = material


class UploadFilesMarkSaved:
    order_id: uuid.UUID
    material: Material
    file_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID, material: Material, file_id: uuid.UUID):
        self.order_id = order_id
        self.material = material
        self.file_id = file_id


class UploadFilesReady:
    order_id: uuid.UUID
    materials_set: []

    def __init__(self, order_id: uuid.UUID, materials_set: []):
        self.order_id = order_id
        self.materials_set = materials_set


class GetInfoFromManager:
    order_id: uuid.UUID
    price: int

    def __init__(self, order_id: uuid.UUID, price: int):
        self.order_id = order_id
        self.price = price


class CreateContract:
    order_id: uuid.UUID
    price: int

    def __init__(self, order_id: uuid.UUID, price: int):
        self.order_id = order_id
        self.price = price


class AsIndividual:
    order_id: uuid.UUID
    full_name: str
    birthday: datetime.datetime
    passport_number: str
    issued_by: str
    issued_by_number: str
    address: str

    def __init__(self, order_id: uuid.UUID, full_name: str, birthday: datetime.datetime, passport_number: str,
                 issued_by: str,
                 issued_by_number: str, address: str):
        self.order_id = order_id
        self.full_name = full_name
        self.birthday = birthday
        self.passport_number = passport_number
        self.issued_by = issued_by
        self.issued_by_number = issued_by_number
        self.address = address


class AsCompany:
    order_id: uuid.UUID
    full_name: str
    position: str
    taxpayer_number: str

    def __init__(self, order_id: uuid.UUID, full_name: str, position: str, taxpayer_number: str):
        self.order_id = order_id
        self.full_name = full_name
        self.position = position
        self.taxpayer_number = taxpayer_number


class AddInfoForContract:
    order_id: uuid.UUID
    data: Any

    def __init__(self, order_id: uuid.UUID, data: Any):
        self.order_id = order_id
        self.data = data


class SendContract:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


class SendContractToManager:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


class CreatePrePayment:
    order_id: uuid.UUID
    price: int

    def __init__(self, order_id: uuid.UUID, price: int):
        self.order_id = order_id
        self.price = price


class PrePaymentComplete:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


class OrderReady:
    order_id: uuid.UUID
    file: str

    def __init__(self, order_id: uuid.UUID, file: str):
        self.order_id = order_id
        self.file = file


class CreateFinalPayment:
    order_id: uuid.UUID
    price: int

    def __init__(self, order_id: uuid.UUID, price: int):
        self.order_id = order_id
        self.price = price


class FinalPaymentComplete:
    order_id: uuid.UUID

    def __init__(self, order_id: uuid.UUID):
        self.order_id = order_id


type Action = (
        Start | CreateOrder | RemoveOrder | SetOrderName | QuestionnaireAnswer | RestartQuestionnaire | ViewFiles | UploadFilesMarkSaved
        | UploadFilesReady | GetInfoFromManager | CreateContract | AsIndividual | AsCompany | AddInfoForContract
        | SendContract | SendContractToManager | CreatePrePayment | PrePaymentComplete | OrderReady | CreateFinalPayment | FinalPaymentComplete)


def transform(self):
    match self.action:
        case Start():
            return state.CreateUser(self.user_id)
        case CreateOrder(order_id=order_id):
            return state.User(self.user_id, user.CreateOrder(order_id))
        case RemoveOrder(order_id=order_id):
            return state.User(self.user_id, user.RemoveOrder(order_id))
        case SetOrderName(order_id=order_id, order_name=order_name):
            return state.User(self.user_id, user.Order(order_id, order.Stage(stageBase.SetOrderName(order_name))))
        case QuestionnaireAnswer(order_id=order_id, response=response):
            return state.User(self.user_id,
                              user.Order(order_id, order.Stage(stageQuest.Materials(materials.Change(response)))))
        case RestartQuestionnaire(order_id=order_id):
            return state.User(self.user_id, user.Order(order_id, order.Stage(stageQuest.RestartQuestionnaire())))
        case ViewFiles(material=material):
            return state.ViewFiles(self.user_id, material)
        case UploadFilesMarkSaved(order_id=order_id, material=material, file_id=file_id):
            return state.User(self.user_id,
                              user.Order(order_id, order.Stage(
                                  stageQuest.Materials(materials.UploadFilesMarkSaved(file_id, material)))))
        case UploadFilesReady(order_id=order_id, materials_set=materials_set):
            return state.User(self.user_id,
                              user.Order(order_id,
                                         order.Stage(stageQuest.Materials(materials.UploadFilesReady(materials_set)))))
        case GetInfoFromManager(order_id=order_id, price=price):
            return state.User(self.user_id, user.Order(order_id, order.Stage(stageMatter.GetInfoFromManager(price))))
        case CreateContract(order_id=order_id, price=price):
            return state.User(self.user_id, user.Order(order_id, order.Stage(stageContract.CreateContract(price))))
        case AsIndividual(order_id=order_id, full_name=full_name, birthday=birthday, passport_number=passport_number,
                          issued_by=issued_by,
                          issued_by_number=issued_by_number, address=address):
            return state.User(self.user_id, user.Order(order_id, order.Stage(
                stageContract.AsIndividual(full_name, birthday, passport_number, issued_by, issued_by_number,
                                           address))))
        case AsCompany(order_id=order_id, full_name=full_name, position=position, taxpayer_number=taxpayer_number):
            return state.User(self.user_id, user.Order(order_id, order.Stage(
                stageContract.AsCompany(full_name, position, taxpayer_number))))
        case AddInfoForContract(order_id=order_id, data=data):
            return state.User(self.user_id,
                              user.Order(order_id,
                                         order.Stage(stageContract.AddContractInfo(contractInfo.Change(data)))))
        case SendContractToManager(order_id=order_id):
            return state.User(self.user_id, user.Order(order_id, order.Stage(stageContract.SendContractToManager())))
        case CreatePrePayment(order_id=order_id, price=price):
            return state.User(self.user_id, user.Order(order_id, order.Stage(stageFinal.CreatePrePayment(price))))
        case PrePaymentComplete(order_id=order_id):
            return state.User(self.user_id, user.Order(order_id, order.Stage(stageFinal.PrePaymentComplete())))
        case OrderReady(order_id=order_id, file=file):
            return state.User(self.user_id, user.Order(order_id, order.Stage(stageFinal.OrderReady(file))))
        case CreateFinalPayment(order_id=order_id, price=price):
            return state.User(self.user_id, user.Order(order_id, order.Stage(stageFinal.CreateFinalPayment(price))))
        case FinalPaymentComplete(order_id=order_id):
            return state.User(self.user_id, user.Order(order_id, order.Stage(stageFinal.FinalPaymentComplete())))


@dataclass
class Command:
    user_id: int
    action: Action

    def __init__(self, user_id: int, action: Action):
        self.user_id = user_id
        self.action = action

    transform = transform
