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
        case SkipToApprovalYes(approval=approval):
            return approval.view(deps)
        case SkipToApprovalNo():
            return {
                'message': "В таком случае, сделайте несколько качественных фотографий основных материалов, из которых производится ваш товар, после чего нажмите на кнопку “Фотографии готовы”",
                'buttons': ["Фотографии готовы"]
            }
        case SkipToApprovalUnknown():
            return {
                'message': "Считаете ли вы, что цвет и фактура материалов достаточно хорошо видны на фотографиях товара?",
                'buttons': ["Да", "Нет"]
            }


def action(self, response):
    match self:
        case SkipToApprovalYes(approval=approval):
            return SkipToApprovalYes(approval.action(response))
        case SkipToApprovalNo():
            match response:
                case SingleResponse.SingleResponseYes():
                    return SkipToApprovalYes(ApprovalUnknown())
        case SkipToApprovalUnknown():
            match response:
                case Response.ResponseYes():
                    return SkipToApprovalYes(ApprovalUnknown())
                case Response.ResponseNo():
                    return SkipToApprovalNo()


def get_set(self, material: Material):
    match self:
        case SkipToApprovalYes(approval=approval):
            return approval.get_set(material)
        case SkipToApprovalNo():
            return None
        case SkipToApprovalUnknown():
            return None


class SkipToApprovalYes:
    approval: Approval

    def __init__(self, approval: Approval):
        self.approval = approval

    view = view
    get_set = get_set
    action = action


class SkipToApprovalNo:
    view = view
    get_set = get_set
    action = action


class SkipToApprovalUnknown:
    view = view
    get_set = get_set
    action = action


type SkipToApproval = SkipToApprovalYes | SkipToApprovalNo | SkipToApprovalUnknown
