# criar a estrutura do banco de dados

from FakePinterest import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    pictures = database.relationship("Posts", backref="user", lazy=True)


class Posts(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    image = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.now())
    id_user = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
