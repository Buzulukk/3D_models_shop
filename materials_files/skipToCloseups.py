import effect
from materials_files.closeups import *
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
        case SkipToCloseupsYes(closeups=closeups):
            return self.closeups.response(active_order, tg_message)
        case SkipToCloseupsNo():
            match tg_message["message"]["text"]:
                case "Замеры готовы":
                    return command.Command(user_id, command.QuestionnaireAnswer(active_order,
                                                                                SingleResponse.SingleResponseYes()))
                case _:
                    return None
        case SkipToCloseupsUnknown():
            match tg_message["message"]["text"]:
                case "Продолжить без замеров":
                    return command.Command(user_id, command.QuestionnaireAnswer(active_order, Response.ResponseYes()))
                case "Я проведу замеры":
                    return command.Command(user_id, command.QuestionnaireAnswer(active_order, Response.ResponseNo()))
                case _:
                    return None


def view(self, deps):
    match self:
        case SkipToCloseupsYes(closeups=closeups):
            return closeups.view(deps)
        case SkipToCloseupsNo():
            return {
                'message': "Хорошо, в таком случае проведите замеры, соберите результаты в файл, после чего нажмите на кнопку “Замеры готовы”",
                'buttons': ["Замеры готовы"]
            }
        case SkipToCloseupsUnknown():
            return {
                'message': "В этих случаях мы рекомендуем всё же провести базовые измерения основных частей товара для получения наилучшего результата. Однако, если вы считаете, что фото содержат достаточно информации о пропорциях товара, вы можете продолжить без замеров.",
                'buttons': ["Продолжить без замеров", "Я проведу замеры"]
            }


def action(self, response):
    match self:
        case SkipToCloseupsYes(closeups=closeups):
            return SkipToCloseupsYes(closeups.action(response))
        case SkipToCloseupsNo():
            match response:
                case SingleResponse.SingleResponseYes():
                    return SkipToCloseupsYes(CloseupsUnknown())
        case SkipToCloseupsUnknown():
            match response:
                case Response.ResponseYes():
                    return SkipToCloseupsYes(CloseupsUnknown())
                case Response.ResponseNo():
                    return SkipToCloseupsNo()


def get_set(self, material: Material):
    match self:
        case SkipToCloseupsYes(closeups=closeups):
            return closeups.get_set(material)
        case SkipToCloseupsNo():
            return None
        case SkipToCloseupsUnknown():
            return None


class SkipToCloseupsYes:
    closeups: Closeups

    def __init__(self, closeups: Closeups):
        self.closeups = closeups

    response = response
    view = view
    get_set = get_set
    action = action


class SkipToCloseupsNo:
    response = response
    view = view
    get_set = get_set
    action = action


class SkipToCloseupsUnknown:
    response = response
    view = view
    get_set = get_set
    action = action


type SkipToCloseups = SkipToCloseupsYes | SkipToCloseupsNo | SkipToCloseupsUnknown
