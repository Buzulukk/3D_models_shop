def create_payment(self):
    pass # Payment magic


class Payment:
    is_payment_done: bool
    info: dict

    def __init__(self, is_payment_done: bool, info: dict):
        self.is_payment_done = is_payment_done
        self.info = info

    pay = create_payment
