import command
import effect


class SetOrderName:
    name: str

    def __init__(self, name: str):
        self.name = name


type Action = SetOrderName


def reduce(self, action: Action):
    match action:
        case SetOrderName(name=name):
            self.name = name
            return [
                effect.View()
            ]


def response(self, active_order, tg_message):
    user_id = tg_message["message"]["chat"]["id"]

    match self.name:
        case "No name":
            return command.Command(user_id, command.SetOrderName(active_order, tg_message["message"]["text"]))
        case _:
            return None


class Base:
    name: str

    def __init__(self, name: str):
        self.name = name

    reduce = reduce
    response = response
