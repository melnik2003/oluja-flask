from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp

un_min = 6
un_max = 20

pass_min = 8
pass_max = 128


class RegistrationForm(FlaskForm):
    username = StringField('Логин',
                           validators=[DataRequired(),
                                       Length(min=un_min, max=un_max,
                                              message=f"Длина от {un_min} до {un_max} символов"),
                                       Regexp('^[A-Za-z0-9._-]+$',
                                              message="Разрешены англ. буквы, цифры и -_.")])
    password = PasswordField('Пароль',
                             validators=[DataRequired(),
                                         Length(min=pass_min, max=pass_max,
                                                message=f"Длина от {pass_min} до {pass_max} символов")])
    confirm_password = PasswordField('Подтвердите пароль',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')
