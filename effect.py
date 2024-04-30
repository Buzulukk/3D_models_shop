from typing import Any
import payment


class Nothing:
    pass


class Message:
    message: str

    def __init__(self, message):
        self.message = message


class MessageWithButtons:
    message: str
    buttons: [str]

    def __init__(self, message: str, buttons: [str]):
        self.message = message
        self.buttons = buttons


class MessageWithLinksAndButtons:
    message: str
    links: dict
    buttons: [str]

    def __init__(self, message: str, links: dict, buttons: [str]):
        self.message = message
        self.links = links
        self.buttons = buttons


class View:
    pass


class StopQuestionnaire:
    pass


class RepeatQuestionnaire:
    pass


class Contract:
    contract: Any  # change to file type later

    def __init__(self, contract: Any):
        self.contract = contract


class Payment:
    payment: payment.Payment

    def __init__(self, payment: payment.Payment):
        self.payment = payment


class File:
    file: str

    def __init__(self, file: str):
        self.file = file


type Effect = (Nothing | Message | MessageWithButtons | MessageWithLinksAndButtons | View | StopQuestionnaire |
               RepeatQuestionnaire | Contract | Payment | File)
