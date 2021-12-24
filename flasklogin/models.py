from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
manager = LoginManager(app)
app.secret_key = 'some_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False,)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(250), unique=True)
    phone = db.Column(db.String(13), unique=True)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text)
    photo = db.Column(db.String(250))