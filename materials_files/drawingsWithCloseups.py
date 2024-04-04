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


def view(self, deps):
    match self:
        case DrawingsWithCloseupsPresent(approval=approval):
            return approval.view(deps)
        case DrawingsWithCloseupsAbsent():
            return [
                effect.QuestionnaireQuestion(
                    "К сожалению, в таком случае невозможно создать качественную 30 модель. Чтобы продолжить, разработайте чертежи и сделайте качественные, отражающие фактуру фото образов материала, после чего нажмите на кнопку “Чертежи и фото образцов готовы”",
                    ["Чертежи и фото образцов готовы"]
                )
            ]
        case DrawingsWithCloseupsUnknown():
            return [
                effect.QuestionnaireQuestion(
                    "Есть ли у вас чертежи и качественные, отражающие цвет и фактуру фото образцов материалов использующихся при производстве товара?",
                    ["Да", "Нет"]
                )
            ]


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

    view = view
    get_set = get_set
    action = action


class DrawingsWithCloseupsAbsent:
    view = view
    get_set = get_set
    action = action


class DrawingsWithCloseupsUnknown:
    view = view
    get_set = get_set
    action = action


type DrawingsWithCloseups = DrawingsWithCloseupsPresent | DrawingsWithCloseupsAbsent | DrawingsWithCloseupsUnknown
