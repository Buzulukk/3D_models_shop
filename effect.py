class Nothing:
    pass


class Message:
    message: str

    def __init__(self, message):
        self.message = message


class QuestionnaireQuestion:
    message: str
    buttons: [str]

    def __init__(self, message: str, buttons: [str]):
        self.message = message
        self.buttons = buttons


type Effect = Nothing | Message | QuestionnaireQuestion
