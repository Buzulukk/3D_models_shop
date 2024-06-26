import effect

from materials_files.approval import *
from materials_files.material import *


class SingleResponse:
    class SingleResponseYes:
        pass


class Response:
    class ResponseYes:
        pass

    class ResponseNo:
        pass


def response(self, active_order, tg_message):
    user_id = tg_message["message"]["chat"]["id"]

    match self:
        case DrawingsWithCloseupsPresent(approval=approval):
            return self.approval.response(active_order, tg_message)
        case DrawingsWithCloseupsAbsent():
            match tg_message["message"]["text"]:
                case "Чертежи и фото образцов готовы":
                    return command.Command(user_id, command.QuestionnaireAnswer(active_order,
                                                                                SingleResponse.SingleResponseYes()))
                case _:
                    return None
        case DrawingsWithCloseupsUnknown():
            match tg_message["message"]["text"]:
                case "Да":
                    return command.Command(user_id, command.QuestionnaireAnswer(active_order, Response.ResponseYes()))
                case "Нет":
                    return command.Command(user_id, command.QuestionnaireAnswer(active_order, Response.ResponseNo()))
                case _:
                    return None


def view(self, deps):
    match self:
        case DrawingsWithCloseupsPresent(approval=approval):
            return approval.view(deps)
        case DrawingsWithCloseupsAbsent():
            return {
                'message': "К сожалению, в таком случае невозможно создать качественную 3D модель. Чтобы продолжить, разработайте чертежи и сделайте качественные, отражающие фактуру фото образов материала, после чего нажмите на кнопку “Чертежи и фото образцов готовы”",
                'buttons': ["Чертежи и фото образцов готовы"]
            }
        case DrawingsWithCloseupsUnknown():
            return {
                'message': "Есть ли у вас чертежи и качественные, отражающие цвет и фактуру фото образцов материалов использующихся при производстве товара?",
                'buttons': ["Да", "Нет"]
            }


def action(self, response):
    match self:
        case DrawingsWithCloseupsPresent(approval=approval):
            return DrawingsWithCloseupsPresent(approval.action(response))
        case DrawingsWithCloseupsAbsent():
            match response:
                case SingleResponse.SingleResponseYes():
                    return DrawingsWithCloseupsPresent(ApprovalUnknown())
        case DrawingsWithCloseupsUnknown():
            match response:
                case Response.ResponseYes():
                    return DrawingsWithCloseupsPresent(ApprovalUnknown())
                case Response.ResponseNo():
                    return DrawingsWithCloseupsAbsent()


def get_set(self, material: Material):
    material_is_drawings_or_closeups = False
    match material:
        case MaterialDrawings():
            material_is_drawings_or_closeups = True
        case MaterialCloseups():
            material_is_drawings_or_closeups = True

    match self:
        case DrawingsWithCloseupsPresent(approval=approval):
            return None if approval.get_set(material) is None \
                else approval.get_set(material) or material_is_drawings_or_closeups
        case DrawingsWithCloseupsAbsent():
            return None
        case DrawingsWithCloseupsUnknown():
            return None


class DrawingsWithCloseupsPresent:
    approval: Approval

    def __init__(self, approval: Approval):
        self.approval = approval

    response = response
    view = view
    get_set = get_set
    action = action


class DrawingsWithCloseupsAbsent:
    response = response
    view = view
    get_set = get_set
    action = action


class DrawingsWithCloseupsUnknown:
    response = response
    view = view
    get_set = get_set
    action = action


type DrawingsWithCloseups = DrawingsWithCloseupsPresent | DrawingsWithCloseupsAbsent | DrawingsWithCloseupsUnknown
