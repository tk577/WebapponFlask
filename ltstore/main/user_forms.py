
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, BooleanField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .model import Profiles


class LoginForm(FlaskForm):
    email = StringField("email: ", validators=[Email(), DataRequired()])
    password1 = PasswordField("Пароль: ", validators=[Length(min=4, max=100), DataRequired()])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField("Имя: ", validators=[Length(min=2, max=50, message="Имя от 2 символов"), DataRequired()])
    lastname = StringField("Фамилия: ", validators=[Length(min=2, max=50, message="Фамилия от 2 символов"), DataRequired()])
    email = StringField("email: ", validators=[Email("Некорректный email"), DataRequired()])
    phone = IntegerField("Номер телефона:+7 ", validators=[DataRequired()])
    password1 = PasswordField("Пароль: ", validators=[DataRequired()])
    psw2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo("password1", message="пароли не совпадают")])
    date = DateField("Дата рождения: ")
    city = StringField("Город: ")

    agreement = BooleanField("С условиями магазина ознакомлен и согласен", validators=[DataRequired()], default=False)

    submit = SubmitField(label='Зарегистрироваться')

    def validate_email(self, email_to_check):
        email = Profiles.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("Пользователь с таким email уже существует! Попробуйте ввести другую электронную почту")

    def validate_phone(self, phone_to_check):
        phone = Profiles.query.filter_by(email=phone_to_check.data).first()
        if phone:
            raise ValidationError("Пользователь с таким номером телефона уже существует!")


class EditProfile(FlaskForm):
    name = StringField("Имя: ")
    lastname = StringField("Фамилия: ")
    email = StringField("email: ")

    submit = SubmitField()


class Post(FlaskForm):
    comment = TextAreaField(validators=[Length(max=1000)])

    submit = SubmitField(label='Отправить')
