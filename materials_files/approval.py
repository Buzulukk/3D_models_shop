import effect

from materials_files import material


class Response:
    class ResponseYes:
        pass

    class ResponseNo:
        pass


def view(self, deps):
    match self:
        case ApprovalYes():
            return [
                effect.Message("Завершение опроса"),
                effect.StopQuestionnaire()
            ]
        case ApprovalNo():
            return [
                effect.Message("В таком случае, чтобы во всём убедиться, я проведу опрос заново"),
                effect.RepeatQuestionnaire()
            ]
        case ApprovalUnknown():
            question_message = "Таким образом, правильно ли мы понимаем, что у вас есть:\n"
            for el in deps['get_set_func']():
                match el:
                    case material.MaterialPhotos():
                        question_message += "• Фото товара\n"
                    case material.MaterialDrawings():
                        question_message += "• Чертежи товара\n"
                    case material.MaterialCloseups():
                        question_message += "• Фото материалов"

            return [
                effect.MessageWithButtons(
                    question_message,
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


def get_set(self, material: material.Material):
    match self:
        case ApprovalYes():
            return False
        case ApprovalNo():
            return False
        case ApprovalUnknown():
            return False


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
