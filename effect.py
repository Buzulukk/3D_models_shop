class Nothing:
    pass


class Message:
    message: str

    def __init__(self, message):
        self.message = message


type Effect = Nothing | Message
