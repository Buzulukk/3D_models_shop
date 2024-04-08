import effect

from contract import *


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


class SendContract:
    pass


type Action = CreateContract | AsIndividual | AsCompany | SendContract


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
                effect.Nothing()
            ]
        case AsCompany(full_name=full_name, position=position, taxpayer_number=taxpayer_number):
            self.contract = CompanyContract(full_name, position, taxpayer_number)
            return [
                effect.Nothing()
            ]
        case SendContract():
            return [
                effect.Message("Это договор на наши услуги. Чтобы продолжить, подпишите его и отправьте."),
                effect.Contract(self.contract)
            ]


class Contract:
    contract: Contract

    def __init__(self, contract: Contract):
        self.contract = contract

    reduce = reduce
