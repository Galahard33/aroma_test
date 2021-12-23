
from wtforms import BooleanField, PasswordField, SubmitField, StringField, Form
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from models import User


class LoginForm(Form):
    login = StringField('Login',
            validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


class RegisterForm(Form):
    login = StringField('Username',
            validators=[DataRequired(), Length(min=3, max=32)])
    password = PasswordField('Password',
            validators=[DataRequired(), Length(min=8, max=64)])
    confirm = PasswordField('Verify password',
            validators=[DataRequired(), EqualTo('password',
            message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
