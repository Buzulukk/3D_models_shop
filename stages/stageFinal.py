import effect
import payment


class CreatePrePayment:
    price: int

    def __init__(self, price: int):
        self.price = price


class PrePaymentComplete:
    pass


type Action = CreatePrePayment | PrePaymentComplete


def reduce(self, action: Action):
    match action:
        case CreatePrePayment(price=price):
            self.payment = payment.Payment(False, {"price": price})
            return [
                effect.Payment(self.payment)
            ]
        case PrePaymentComplete():
            self.payment.is_payment_done = True
            return [
                effect.Message(
                    "Мы получили вашу предоплату и ваш заказ взят в работу. Как только всё будет готово, мы тут же вас оповестим! Помните, что по всем вопросам вы можете обращаться в нашу службу заботы о клиентах.")
            ]


class Final:
    payment: payment.Payment

    def __init__(self, payment: payment.Payment):
        self.payment = payment

    reduce = reduce
