import command
import effect

from materials_files import material


class Response:
    class ResponseYes:
        pass

    class ResponseNo:
        pass


def response(self, active_order, tg_message):
    user_id = tg_message["message"]["chat"]["id"]

    match self:
        case ApprovalYes():
            return None
        case ApprovalNo():
            return None
        case ApprovalUnknown():
            match tg_message["message"]["text"]:
                case "Верно":
                    return command.Command(user_id, command.QuestionnaireAnswer(active_order, Response.ResponseYes()))
                case "Не совсем":
                    return command.Command(user_id, command.QuestionnaireAnswer(active_order, Response.ResponseNo()))
                case _:
                    return None


def view(self, deps):
    match self:
        case ApprovalYes():
            return {
                'message': "Сейчас вам нужно будет загрузить файлы необходимые для создания модели"
            }
        case ApprovalNo():
            return {
                'message': "В таком случае, чтобы во всём убедиться, я проведу опрос заново"
            }
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

            return {
                'message': question_message,
                'buttons': ["Верно", "Не совсем"]
            }


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
    response = response
    view = view
    get_set = get_set
    action = action


class ApprovalNo:
    response = response
    view = view
    get_set = get_set
    action = action


class ApprovalUnknown:
    response = response
    view = view
    get_set = get_set
    action = action


type Approval = ApprovalYes | ApprovalNo | ApprovalUnknown
