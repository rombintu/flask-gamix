# Подключаем нужные библиотеки (https://flask-sqlalchemy.palletsprojects.com/en/2.x/ - документация)
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
# https://werkzeug.palletsprojects.com/en/2.0.x/ (для создания паролей как в нормальных системах)
from werkzeug.security import generate_password_hash, check_password_hash
# Подключаем модель юзера из моделей (для регистрации и логина) и базу данных
from .models import User
from . import db
# (https://flask.palletsprojects.com/en/1.1.x/tutorial/views/) либа для логинов и отслеживания того что юзер зашел
auth = Blueprint('auth', __name__)

# когда юзер переходит по этой ссылке в системе '/login', то ему возвращается 'login.html' 
@auth.route('/login')
def login():
    return render_template('login.html')

# тож самое
@auth.route('/signup')
def signup():
    return render_template('signup.html')

# тож самое, только за юзером перестает следить блюпринт
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.profile'))

# POST METHODS, POST это запрос на изменение данных, GET на получение
# когда юзер находясь по маршруту /signup нажимает на отправку формы, то происходит эта функция
@auth.route('/signup', methods=['POST'])
def signup_post():
    # из формы забираются данные 
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    # Баллы при регистрации равны нулю
    score = 0
    # 
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database


    # Flash это сообщение об ошибке, которое кидается пользователю
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # Создается новый объект пользователя на основе нашей модели импортированной ранее. 
    # Также создается хеш пароля и он сохраняется, а не сам пароль
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), role="user", score=score)
    # добавляем нового пользователя в бд
    db.session.add(new_user)
    # подтверждение действий с бд
    db.session.commit()
    # Кидаем пользователя на логин
    return redirect(url_for('auth.login'))

# Почти все тоже самое
@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # Проверка на то что юзер существует и пароль совпадает
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    # логиним юзера в блюпринте и если нужно, запоминаем его
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))