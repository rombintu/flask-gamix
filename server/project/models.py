from flask_login import UserMixin
from . import db

# Связующая табличка многие ко многим между Тестами и Пользователями
user_questions = db.Table('user_questions',
    # Колонка user_id INT FOREIGN KEY User.id
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('questions.id'))
    )

# Модель Пользователя
class User(UserMixin, db.Model):
    # айди INT PRIMARY KEY
    id = db.Column(db.Integer, primary_key=True) # Первичный ключ
    # email VARCHAR(100) UNIQUE
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    role = db.Column(db.String(10))
    score = db.Column(db.Integer)
    # Доп колонка для связи с тестами
    user_questions = db.relationship('Questions', 
        secondary=user_questions, 
        # lazy='dynamic',
        backref=db.backref('user_questions', lazy='dynamic')
        )

# Модель тестов
class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Первичный ключ
    title = db.Column(db.String(100), unique=True)
    text1 = db.Column(db.String(200))
    answer1 = db.Column(db.String(20))
    text2 = db.Column(db.String(200))
    answer2 = db.Column(db.String(20))
    text3 = db.Column(db.String(200))
    answer3 = db.Column(db.String(20))

    # Инициализацию прописываем для создания нового теста без гемора
    def __init__(self, title, text1, answer1, text2, answer2, text3, answer3):
        self.title = title
        self.text1 = text1
        self.answer1 = answer1
        self.text2 = text2
        self.answer2 = answer2
        self.text3 = text3
        self.answer3 = answer3
    # метод возвращающий айди теста
    def get_id(self):
        return self.id
