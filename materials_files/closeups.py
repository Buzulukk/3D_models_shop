import effect
from materials_files.approval import *
from materials_files.skipToApproval import *
from materials_files.material import *


class Response:
    class ResponseYes:
        pass

    class ResponseNo:
        pass


def view(self):
    match self:
        case CloseupsPresent(approval=approval):
            return approval.view()
        case CloseupsAbsent(skip=skip):
            return skip.view()
        case CloseupsUnknown():
            return [
                effect.QuestionnaireQuestion(
                    "Есть ли у вас качественные, отражающие цвет и фактуру фото образцов материалов использующихся при производстве?",
                    ["Да", "Нет"]
                )
            ]


def action(self, response):
    match self:
        case CloseupsPresent(approval=approval):
            return CloseupsPresent(approval.action(response))
        case CloseupsAbsent(skip=skip):
            return CloseupsAbsent(skip.action(response))
        case CloseupsUnknown():
            match response:
                case Response.ResponseYes():
                    return CloseupsPresent(ApprovalUnknown())
                case Response.ResponseNo():
                    return CloseupsAbsent(SkipToApprovalUnknown())


def get_set(self, material: Material):
    material_is_closeups = False
    match material:
        case MaterialCloseups():
            material_is_closeups = True

    match self:
        case CloseupsPresent(approval=approval):
            return None if approval.get_set(material) is None \
                else approval.get_set(material) or material_is_closeups
        case CloseupsAbsent(skip=skip):
            return None if skip.get_set(material) is None \
                else skip.get_set(material) or material_is_closeups
        case CloseupsUnknown():
            return None


class CloseupsPresent:
    approval: Approval

    def __init__(self, approval: Approval):
        self.approval = approval

    view = view
    get_set = get_set
    action = action


class CloseupsAbsent:
    skip: SkipToApproval

    def __init__(self, skip: SkipToApproval):
        self.skip = skip

    view = view
    get_set = get_set
    action = action


class CloseupsUnknown:
    view = view
    get_set = get_set
    action = action


type Closeups = CloseupsPresent | CloseupsAbsent | CloseupsUnknown
