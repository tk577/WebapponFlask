
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, TextAreaField, DateTimeField, SubmitField, SelectField
from wtforms.validators import DataRequired
from datetime import datetime

class AddItem(FlaskForm):

    item_brand = StringField('Фирма: ', validators=[DataRequired()])
    item_name = StringField('Название товара: ', validators=[DataRequired()])
    category = SelectField(label="Категория: ", choices=['Ноутбуки', 'Зарядные устройства', 'Сумки',
                                                         'Клавиатуры', 'Комплектующие и запчасти', 'ПО'])
    barcode = StringField('Штрихкод: ', validators=[DataRequired()])
    price = IntegerField('Цена: ', validators=[DataRequired()])
    display = StringField('Экран: ')
    cpu = StringField('Процессор: ')
    rom = StringField('Оперативная память, Гб: ')
    ram = StringField('Встроенная память, Гб: ')
    description = TextAreaField('Описание: ')
    date = DateTimeField('Время добавления: ', default=datetime.now())
    quantity = IntegerField('Количество: ', validators=[DataRequired()])
    image = FileField('Изображение', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Пожалуйста, используйте форматы: png, jpg, jpeg!')])

    submit = SubmitField('Добавить')
