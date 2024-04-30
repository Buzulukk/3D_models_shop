import command
import effect
from materials_files.closeups import *
from materials_files.skipToCloseups import *
from materials_files.material import *


class Response:
    class ResponseYes:
        pass

    class ResponseNo:
        pass


def response(self, active_order, tg_message):
    user_id = tg_message["message"]["chat"]["id"]

    match self:
        case DrawingsPresent(closeups=closeups):
            return self.closeups.response(active_order, tg_message)
        case DrawingsAbsent(skip=skip):
            return self.skip.response(active_order, tg_message)
        case DrawingsUnknown():
            match tg_message["message"]["text"]:
                case "Да":
                    return command.Command(user_id, command.QuestionnaireAnswer(active_order, Response.ResponseYes()))
                case "Нет":
                    return command.Command(user_id, command.QuestionnaireAnswer(active_order, Response.ResponseNo()))
                case _:
                    return None

def view(self, deps):
    match self:
        case DrawingsPresent(closeups=closeups):
            return closeups.view(deps)
        case DrawingsAbsent(skip=skip):
            return skip.view(deps)
        case DrawingsUnknown():
            return {
                'message': "Есть ли у вас чертежи товара с указанием размеров?",
                'buttons': ["Да", "Нет"]
            }


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
                else skip.get_set(material) or not material_is_drawings
        case DrawingsUnknown():
            return None


class DrawingsPresent:
    closeups: Closeups

    def __init__(self, closeups: Closeups):
        self.closeups = closeups

    response = response
    view = view
    get_set = get_set
    action = action


class DrawingsAbsent:
    skip: SkipToCloseups

    def __init__(self, skip: SkipToCloseups):
        self.skip = skip

    response = response
    view = view
    get_set = get_set
    action = action


class DrawingsUnknown:
    response = response
    view = view
    get_set = get_set
    action = action


type Drawings = DrawingsPresent | DrawingsAbsent | DrawingsUnknown
