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


def view(self, deps):
    match self:
        case SkipToCloseupsYes(closeups=closeups):
            return closeups.view(deps)
        case SkipToCloseupsNo():
            return [
                effect.QuestionnaireQuestion(
                    "Хорошо, в таком случае проведите замеры, соберите результаты в файл, после чего нажмите на кнопку “Замеры готовы”",
                    ["Замеры готовы"]
                )
            ]
        case SkipToCloseupsUnknown():
            return [
                effect.QuestionnaireQuestion(
                    "В этих случаях мы рекомендуем всё же провести базовые измерения основных частей товара для получения наилучшего результата. Однако, если вы считаете, что фото содержат достаточно информации о пропорциях товара, вы можете продолжить без замеров.",
                    ["Продолжить без замеров", "Я проведу замеры"]
                )
            ]


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

    view = view
    get_set = get_set
    action = action


class SkipToCloseupsNo:
    view = view
    get_set = get_set
    action = action


class SkipToCloseupsUnknown:
    view = view
    get_set = get_set
    action = action


type SkipToCloseups = SkipToCloseupsYes | SkipToCloseupsNo | SkipToCloseupsUnknown
