from typing import Any


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


class StopQuestionnaire:
    pass


class RepeatQuestionnaire:
    pass


class Contract:
    contract: Any  # change to file type later

    def __init__(self, contract: Any):
        self.contract = contract


type Effect = Nothing | Message | MessageWithButtons | StopQuestionnaire | RepeatQuestionnaire | Contract
