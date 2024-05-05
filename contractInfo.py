import datetime
from typing import Any

import command
import effect


class Change:
    data: Any

    def __init__(self, data: Any):
        self.data = data


type Action = Change


def ask_info_for_contract(self):
    match self:
        case IndividualContract(full_name=full_name, birthday=birthday, passport_number=passport_number,
                                issued_by=issued_by, issued_by_number=issued_by_number, address=address):
            if not full_name:
                return [effect.Message("Пожалуйста, укажите ФИО")]
            elif not birthday:
                return [effect.Message("Пожалуйста, укажите дату рождения")]
            elif not passport_number:
                return [effect.Message("Пожалуйста, укажите серию и номер паспорта")]
            elif not issued_by:
                return [effect.Message("Пожалуйста, укажите кем и когда выдан паспорт")]
            elif not issued_by_number:
                return [effect.Message("Пожалуйста, укажите код подразделения")]
            elif not address:
                return [effect.Message("Пожалуйста, укажите адрес прописки")]
            else:
                return [
                    effect.Message("Это договор на наши услуги. Чтобы продолжить, подпишите его и отправьте."),
                    effect.Contract(self)
                ]
        case CompanyContract(full_name=full_name, position=position, taxpayer_number=taxpayer_number):
            if not full_name:
                return [effect.Message("Пожалуйста, укажите ФИО лица, подписывающего договор")]
            elif not position:
                return [effect.Message("Пожалуйста, укажите должность лица, подписывающего договор (как в уставе)")]
            elif not taxpayer_number:
                return [effect.Message("Пожалуйста, укажите ИНН")]
            else:
                return [
                    effect.Message("Это договор на наши услуги. Чтобы продолжить, подпишите его и отправьте."),
                    effect.Contract(self)
                ]


def reduce(self, action: Action):
    match action:
        case Change(data=data):
            match self:
                case IndividualContract(full_name=full_name, birthday=birthday, passport_number=passport_number,
                                        issued_by=issued_by, issued_by_number=issued_by_number, address=address):
                    if not full_name:
                        self.full_name = data
                        return [effect.AskInfoForContract()]
                    elif not birthday:
                        self.birthday = data
                        return [effect.AskInfoForContract()]
                    elif not passport_number:
                        self.passport_number = data
                        return [effect.AskInfoForContract()]
                    elif not issued_by:
                        self.issued_by = data
                        return [effect.AskInfoForContract()]
                    elif not issued_by_number:
                        self.issued_by_number = data
                        return [effect.AskInfoForContract()]
                    elif not address:
                        self.address = data
                        return [effect.AskInfoForContract()]
                    else:
                        return [effect.AskInfoForContract()]
                case CompanyContract(full_name=full_name, position=position, taxpayer_number=taxpayer_number):
                    if not full_name:
                        self.full_name = data
                        return [effect.AskInfoForContract()]
                    elif not position:
                        self.position = data
                        return [effect.AskInfoForContract()]
                    elif not taxpayer_number:
                        self.taxpayer_number = data
                        return [effect.AskInfoForContract()]
                    else:
                        return [effect.AskInfoForContract()]


def response(self, active_order, tg_message):
    user_id = tg_message["message"]["chat"]["id"]

    return command.Command(user_id, command.AddInfoForContract(active_order, tg_message["message"]["text"]))


class IndividualContract:
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

    reduce = reduce
    response = response
    ask_info_for_contract = ask_info_for_contract


class CompanyContract:
    full_name: str
    position: str
    taxpayer_number: str

    def __init__(self, full_name: str, position: str, taxpayer_number: str):
        self.full_name = full_name
        self.position = position
        self.taxpayer_number = taxpayer_number

    reduce = reduce
    response = response
    ask_info_for_contract = ask_info_for_contract


type ContractInfo = IndividualContract | CompanyContract
