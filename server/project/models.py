from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role = db.Column(db.String(10))
    score = db.Column(db.Integer)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    text1 = db.Column(db.String(200))
    answer1 = db.Column(db.String(20))
    text2 = db.Column(db.String(200))
    answer2 = db.Column(db.String(20))
    text3 = db.Column(db.String(200))
    answer3 = db.Column(db.String(20))

    def __init__(self, title, text1, answer1, text2, answer2, text3, answer3):
        self.title = title
        self.text1 = text1
        self.answer1 = answer1
        self.text2 = text2
        self.answer2 = answer2
        self.text3 = text3
        self.answer3 = answer3

    def get_id(self):
        return self.id