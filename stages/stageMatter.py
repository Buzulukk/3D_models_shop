import effect


class GetInfoFromManager:
    price: int

    def __init__(self, price: int):
        self.price = price


type Action = GetInfoFromManager


def reduce(self, action: Action):
    match action:
        case GetInfoFromManager(price=price):
            self.price = price
            return [
                effect.MessageWithButtons(
                    "Отличные новости! Расчет по вашей модели готов, её создание будет стоить " + str(price) + " ₽.",
                    ["Утвердить", "Отменить заказ"]
                )
            ]


class Matter:
    price: int

    reduce = reduce
