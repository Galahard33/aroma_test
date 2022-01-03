from flask_user import UserMixin, LoginManager
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
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    phone = db.Column(db.String(13), unique=True, nullable=True)
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


