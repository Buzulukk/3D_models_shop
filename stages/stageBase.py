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
                effect.Nothing()
            ]


class Base:
    name: str

    def __init__(self, name: str):
        self.name = name

    reduce = reduce
