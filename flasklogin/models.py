from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from slugify import slugify


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
    post = db.relationship('Blog', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.login

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    blog = db.relationship('Blog', backref='category', lazy=True)

    def __repr__(self):
        return '<Category %r>' % self.title

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text)
    photo = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)


