
from flask import request
import stripe

stripe.api_key = 'your_test_key'


class PaymentRouteException(Exception):

    def __str__(self):
        return f'Ошибка при переходе на сайт оплаты.'


class CheckoutSession(PaymentRouteException):

    def payment_method_types(self):
        payment_method_types = ['card']
        return payment_method_types

    def mode_payment(self):
        mode = 'payment'
        return mode

    def success_data(self, success):
        success_url = request.host_url + success
        return success_url

    def cancel_data(self, cancel):
        cancel_url = request.host_url + cancel
        return cancel_url


class PaymentCard(PaymentRouteException):
    def __init__(self, total_price):
        self._total_price = total_price

    def pay_info(self):
        line_items = [
            {
                'price_data': {
                    'product_data': {
                        'name': 'Итоговая цена'
                    },
                    'unit_amount': 100 * self._total_price,
                    'currency': 'rub',
                },
                'quantity': 1,
            },
        ]
        return line_items


def checkout_session_func(total_price, success, cancel):
    line_items = PaymentCard(total_price).pay_info()
    data_session = CheckoutSession()
    payment_method_types = data_session.payment_method_types()
    mode = data_session.mode_payment()
    success_url = data_session.success_data(success)
    cancel_url = data_session.cancel_data(cancel)

    return stripe.checkout.Session.create(line_items=line_items,
                                          payment_method_types=payment_method_types,
                                          mode=mode,
                                          success_url=success_url,
                                          cancel_url=cancel_url)
