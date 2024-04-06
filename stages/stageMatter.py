import effect


class SendInfoToManager:
    pass


type Action = SendInfoToManager


def reduce(self, action: Action):
    match action:
        case SendInfoToManager():
            return [
                effect.Message(
                    "Отлично! Ваш заказ принят на расчёт стоимости. Мы свяжемся с вами в течении одного рабочего дня.")
            ]


class Matter:
    reduce = reduce
