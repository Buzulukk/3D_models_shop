import command
import effect
from materials_files.approval import *
from materials_files.skipToApproval import *
from materials_files.material import *


class Response:
    class ResponseYes:
        pass

    class ResponseNo:
        pass


def response(self, active_order, tg_message):
    user_id = tg_message["message"]["chat"]["id"]

    match self:
        case CloseupsPresent(approval=approval):
            return self.approval.response(active_order, tg_message)
        case CloseupsAbsent(skip=skip):
            return self.skip.response(active_order, tg_message)
        case CloseupsUnknown():
            match tg_message["message"]["text"]:
                case "Да":
                    return command.Command(user_id, command.QuestionnaireAnswer(active_order, Response.ResponseYes()))
                case "Нет":
                    return command.Command(user_id, command.QuestionnaireAnswer(active_order, Response.ResponseNo()))
                case _:
                    return None


def view(self, deps):
    match self:
        case CloseupsPresent(approval=approval):
            return approval.view(deps)
        case CloseupsAbsent(skip=skip):
            return skip.view(deps)
        case CloseupsUnknown():
            return {
                'message': "Есть ли у вас качественные, отражающие цвет и фактуру фото образцов материалов использующихся при производстве?",
                'buttons': ["Да", "Нет"]
            }


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
                else skip.get_set(material)
        case CloseupsUnknown():
            return None


class CloseupsPresent:
    approval: Approval

    def __init__(self, approval: Approval):
        self.approval = approval

    response = response
    view = view
    get_set = get_set
    action = action


class CloseupsAbsent:
    skip: SkipToApproval

    def __init__(self, skip: SkipToApproval):
        self.skip = skip

    response = response
    view = view
    get_set = get_set
    action = action


class CloseupsUnknown:
    response = response
    view = view
    get_set = get_set
    action = action


type Closeups = CloseupsPresent | CloseupsAbsent | CloseupsUnknown
