import effect


class SendInfoToManager:
    pass


class GetInfoFromManager:
    price: int

    def __init__(self, price: int):
        self.price = price


type Action = SendInfoToManager | GetInfoFromManager


def reduce(self, action: Action):
    match action:
        case SendInfoToManager():
            return [
                effect.Message(
                    "Отлично! Ваш заказ принят на расчёт стоимости. Мы свяжемся с вами в течении одного рабочего дня.")
            ]
        case GetInfoFromManager(price=price):
            return [
                effect.MessageWithButtons(
                    "Отличные новости! Расчет по вашей модели готов, её создание будет стоить " + str(price) + " ₽.",
                    ["Утвердить", "Отменить заказ"]
                )
            ]


class Matter:
    reduce = reduce
