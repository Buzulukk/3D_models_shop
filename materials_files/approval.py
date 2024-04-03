import effect

from materials_files.material import Material


class Response:
    class ResponseYes:
        pass

    class ResponseNo:
        pass


def view(self):
    match self:
        case ApprovalYes():
            return [
                effect.Message("Завершение опроса")
            ]
        case ApprovalNo():
            return [
                effect.Message("В таком случае, чтобы во всём убедиться, я проведу опрос заново")
            ]
        case ApprovalUnknown():
            return [
                effect.QuestionnaireQuestion(
                    "Таким образом, правильно ли мы понимаем, что у вас есть:",
                    ["Верно", "Не совсем"]
                )
            ]


def action(self, response):
    match self:
        case ApprovalYes():
            return ApprovalYes()
        case ApprovalNo():
            return ApprovalNo()
        case ApprovalUnknown():
            match response:
                case Response.ResponseYes():
                    return ApprovalYes()
                case Response.ResponseNo():
                    return ApprovalNo()


def get_set(self, material: Material):
    match self:
        case ApprovalYes():
            return False
        case ApprovalNo():
            return None
        case ApprovalUnknown():
            return None


class ApprovalYes:
    view = view
    get_set = get_set
    action = action


class ApprovalNo:
    view = view
    get_set = get_set
    action = action


class ApprovalUnknown:
    view = view
    get_set = get_set
    action = action


type Approval = ApprovalYes | ApprovalNo | ApprovalUnknown
