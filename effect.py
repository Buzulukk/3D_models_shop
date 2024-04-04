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


class StopQuestionnaire:
    pass


class MaterialsSet:
    materials_set: []

    def __init__(self, materials_set: []):
        self.materials_set = materials_set


type Effect = Nothing | Message | QuestionnaireQuestion | StopQuestionnaire | MaterialsSet
