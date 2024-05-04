import command
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


def response(self, active_order, tg_message):
    user_id = tg_message["message"]["chat"]["id"]

    match tg_message["message"]["text"]:
        case "Утвердить":
            return command.Command(user_id, command.CreateContract(active_order, self.price))
        case "Отменить заказ":
            return command.Command(user_id, command.RemoveOrder(active_order))
        case _:
            return None


class Matter:
    price: int

    reduce = reduce
    response = response
