import effect
from materials_files.closeups import *
from materials_files.skipToCloseups import *
from materials_files.material import *


class Response:
    class ResponseYes:
        pass

    class ResponseNo:
        pass


def view(self):
    match self:
        case DrawingsPresent(closeups=closeups):
            return closeups.view()
        case DrawingsAbsent(skip=skip):
            return skip.view()
        case DrawingsUnknown():
            return [
                effect.QuestionnaireQuestion(
                    "Есть ли у вас чертежи товара с указанием размеров?",
                    ["Да", "Нет"]
                )
            ]


def action(self, response):
    match self:
        case DrawingsPresent(closeups=closeups):
            return DrawingsPresent(closeups.action(response))
        case DrawingsAbsent(skip=skip):
            return DrawingsAbsent(skip.action(response))
        case DrawingsUnknown():
            match response:
                case Response.ResponseYes():
                    return DrawingsPresent(CloseupsUnknown())
                case Response.ResponseNo():
                    return DrawingsAbsent(SkipToCloseupsUnknown())


def get_set(self, material: Material):
    material_is_drawings = False
    match material:
        case MaterialDrawings():
            material_is_drawings = True

    match self:
        case DrawingsPresent(closeups=closeups):
            return None if closeups.get_set(material) is None \
                else closeups.get_set(material) or material_is_drawings
        case DrawingsAbsent(skip=skip):
            return None if skip.get_set(material) is None \
                else skip.get_set(material) or material_is_drawings
        case DrawingsUnknown():
            return None


class DrawingsPresent:
    closeups: Closeups

    def __init__(self, closeups: Closeups):
        self.closeups = closeups

    view = view
    get_set = get_set
    action = action


class DrawingsAbsent:
    skip: SkipToCloseups

    def __init__(self, skip: SkipToCloseups):
        self.skip = skip

    view = view
    get_set = get_set
    action = action


class DrawingsUnknown:
    view = view
    get_set = get_set
    action = action


type Drawings = DrawingsPresent | DrawingsAbsent | DrawingsUnknown
