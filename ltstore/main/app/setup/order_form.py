# Форма для добавления в корзину и ее обработка

from wtforms import StringField, IntegerField, SelectField, SubmitField
from flask_wtf import FlaskForm


class AddToCart(FlaskForm):
    submit = SubmitField("Купить")
    submit_del = SubmitField("Убрать")


class OrderData(FlaskForm):
    client_name = StringField("Получатель: ")
    email = StringField("email: ")
    phone = IntegerField("Номер телефона: ")
    delivery = SelectField("Способ получения", choices=['Доставка курьером', 'Самовывоз'])
    payment = SelectField("Способ оплаты", choices=['Онлайн оплата', 'Наличными при получении'])

    submit_pay = SubmitField('Заказать')


class PromoCodeForm(FlaskForm):
    code = StringField("Промокод: ")

    submit_code = SubmitField('Применить')
