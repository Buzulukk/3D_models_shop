import contractInfo
import effect
import payment

from contractInfo import *
from payment import Payment


class CreateContract:
    price: int

    def __init__(self, price: int):
        self.price = price


class AsIndividual:
    full_name: str
    birthday: datetime.datetime
    passport_number: str
    issued_by: str
    issued_by_number: str
    address: str

    def __init__(self, full_name: str, birthday: datetime.datetime, passport_number: str, issued_by: str,
                 issued_by_number: str, address: str):
        self.full_name = full_name
        self.birthday = birthday
        self.passport_number = passport_number
        self.issued_by = issued_by
        self.issued_by_number = issued_by_number
        self.address = address


class AsCompany:
    full_name: str
    position: str
    taxpayer_number: str

    def __init__(self, full_name: str, position: str, taxpayer_number: str):
        self.full_name = full_name
        self.position = position
        self.taxpayer_number = taxpayer_number


class SendContractToManager:
    pass


class CreatePrePayment:
    price: int

    def __init__(self, price: int):
        self.price = price


class PrePaymentComplete:
    pass


class ContractInfo:
    action: contractInfo.Action

    def __init__(self, action: contractInfo.Action):
        self.action = action


type Action = (CreateContract | AsIndividual | AsCompany | SendContractToManager | CreatePrePayment |
               PrePaymentComplete | ContractInfo)


def reduce(self, action: Action):
    match action:
        case CreateContract(price=price):
            return [
                effect.MessageWithButtons(
                    "Отлично. Обращаем ваше внимание, что мы работаем по договору. Разработка 3D модели начинается сразу после внесение предоплаты в размере 50% (в вашем случае: " + str(
                        price / 2) + " ₽). Скажите, вы хотели бы заключить договор на физическое лицо или юридическое лицо?",
                    ["Физлицо", "Юрлицо"]
                )
            ]
        case AsIndividual(full_name=full_name, birthday=birthday, passport_number=passport_number, issued_by=issued_by,
                          issued_by_number=issued_by_number, address=address):
            self.contract = IndividualContract(full_name, birthday, passport_number, issued_by, issued_by_number,
                                               address)
            return [
                effect.Message("Вам необходимо указать некоторые данные для составления контракта"),
            ]
        case AsCompany(full_name=full_name, position=position, taxpayer_number=taxpayer_number):
            self.contract = CompanyContract(full_name, position, taxpayer_number)
            return [
                effect.Message("Вам необходимо указать некоторые данные для составления контракта"),
            ]
        case SendContractToManager():
            return [
                effect.Message(
                    "Отлично. Договор отправлен для проверки менеджеру. Это займёт не больше часа в рабочее время, после чего мы тут-же с вами свяжемся.")
            ]
        case CreatePrePayment(price=price):
            self.payment = payment.Payment(False, {"price": price})
            return [
                effect.Payment(self.payment)
            ]
        case PrePaymentComplete():
            self.payment.is_payment_done = True
            return [
                effect.Message(
                    "Мы получили вашу предоплату и ваш заказ взят в работу. Как только всё будет готово, мы тут же вас оповестим! Помните, что по всем вопросам вы можете обращаться в нашу службу заботы о клиентах.")
            ]
        case ContractInfo(action=action):
            return self.contract.reduce(action)


def ask_info_for_contract(self):
    return self.contract.ask_info_for_contract()


class Contract:
    contract: ContractInfo
    payment: Payment

    def __init__(self, contract: ContractInfo, payment: Payment):
        self.contract = contract
        self.payment = payment

    reduce = reduce
    ask_info_for_contract = ask_info_for_contract
