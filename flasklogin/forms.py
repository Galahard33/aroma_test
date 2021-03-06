from flask_ckeditor import CKEditorField
from wtforms import BooleanField, PasswordField, SubmitField, StringField, Form, TextField, FileField, TextAreaField, \
    SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from models import Category


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
    email = StringField('Email',
                      validators=[DataRequired(), Email(), Length(min=6, max=40)])
    phone = StringField('Номер телефона',
            validators=[DataRequired(), Length(min=13, max=13,
            message='Введите телефон в формате +375...')])
    password = PasswordField('Password',
            validators=[DataRequired(), Length(min=8, max=64)])
    confirm = PasswordField('Verify password',
            validators=[DataRequired(), EqualTo('password',
            message='Пароли должны совпадать')])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)


class BlogForm(Form):
    title = StringField('Заголовок',
            validators=[DataRequired(), Length(min=3, max=350)])
    text = CKEditorField('post',
                      validators=[DataRequired()])
    photo_path = StringField('путь')
    category = SelectField (u'Choose')
    slug = StringField('url')

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.category.choices = [(obj.id, obj.title) for obj in Category.query.order_by('title')]


