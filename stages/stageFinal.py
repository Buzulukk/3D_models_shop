import effect
import payment


class CreatePrePayment:
    price: int

    def __init__(self, price: int):
        self.price = price


class PrePaymentComplete:
    pass


class OrderReady:
    file: str

    def __init__(self, file: str):
        self.file = file


class CreateFinalPayment:
    price: int

    def __init__(self, price: int):
        self.price = price


class FinalPaymentComplete:
    pass


type Action = CreatePrePayment | PrePaymentComplete | OrderReady | CreateFinalPayment | FinalPaymentComplete


def reduce(self, action: Action):
    match action:
        case CreatePrePayment(price=price):
            self.pre_payment = payment.Payment(False, {"price": price / 2.0})
            return [
                effect.Payment(self.pre_payment)
            ]
        case PrePaymentComplete():
            self.pre_payment.is_payment_done = True
            return [
                effect.Message(
                    "Мы получили вашу предоплату и ваш заказ взят в работу. Как только всё будет готово, мы тут же вас оповестим! Помните, что по всем вопросам вы можете обращаться в нашу службу заботы о клиентах.")
            ]
        case OrderReady(file=file):
            return [
                effect.File(file),
                effect.MessageWithLinksAndButtons(
                    "Отличные новости, ваша модель готова! Чтобы быстро на неё посмотреть, используйте этот сайт. После этого сообщите нам, удовлетворены ли вы качеством модели.",
                    {(82, 91): "https://gltf-viewer.donmccurdy.com/"},
                    ["Утвердить", "Требуются правки"]
                )
            ]
        case CreateFinalPayment(price=price):
            self.final_payment = payment.Payment(False, {"price": price / 2.0})
            return [
                effect.Message(
                    "В таком случае, были рады помочь вам в создании этой модели! Оплатите вторую часть её разработки."),
                effect.Payment(self.final_payment)
            ]
        case FinalPaymentComplete():
            self.final_payment.is_payment_done = True
            return [
                effect.Message("Благодарим за сотрудничество")
            ]


class Final:
    pre_payment: payment.Payment
    final_payment: payment.Payment

    def __init__(self, pre_payment: payment.Payment, final_payment: payment.Payment):
        self.pre_payment = pre_payment
        self.final_payment = final_payment

    reduce = reduce
