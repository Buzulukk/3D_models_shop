import command
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


class AddContractInfo:
    action: contractInfo.Action

    def __init__(self, action: contractInfo.Action):
        self.action = action


type Action = (CreateContract | AsIndividual | AsCompany | SendContractToManager | AddContractInfo)


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
                effect.AskInfoForContract()
            ]
        case AsCompany(full_name=full_name, position=position, taxpayer_number=taxpayer_number):
            self.contract = CompanyContract(full_name, position, taxpayer_number)
            return [
                effect.Message("Вам необходимо указать некоторые данные для составления контракта"),
                effect.AskInfoForContract()
            ]
        case SendContractToManager():
            return [
                effect.Message(
                    "Отлично. Договор отправлен для проверки менеджеру. Это займёт не больше часа в рабочее время, после чего мы тут-же с вами свяжемся.")
            ]
        case AddContractInfo(action=action):
            return self.contract.reduce(action)


def response(self, active_order, tg_message):
    user_id = tg_message["message"]["chat"]["id"]

    if self.contract is not None:
        return self.contract.response(active_order, tg_message)
    else:
        match tg_message["message"]["text"]:
            case "Физлицо":
                return command.Command(user_id, command.AsIndividual(active_order, None, None, None, None, None))
            case "Юрлицо":
                return command.Command(user_id, command.AsCompany(active_order, None, None, None))
            case _:
                return None


def ask_info_for_contract(self):
    return self.contract.ask_info_for_contract()


class Contract:
    contract: ContractInfo

    def __init__(self, contract: ContractInfo):
        self.contract = contract

    reduce = reduce
    response = response
    ask_info_for_contract = ask_info_for_contract
