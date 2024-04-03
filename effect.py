from materials_files import material


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


class MaterialsSet:
    materials_set: set[material.Material]

    def __init__(self, materials_set: set[material.Material]):
        self.materials_set = materials_set


type Effect = Nothing | Message | QuestionnaireQuestion | MaterialsSet
