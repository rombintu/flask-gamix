# (https://flask.palletsprojects.com/en/1.1.x/tutorial/views/) либа для логинов и отслеживания того что юзер зашел
from flask import Blueprint, render_template, request, redirect, flash, url_for
# Либы которые проверяют что юзер зашел в систему и которые возвращают иформацию о текущем юзере
from flask_login import login_required, current_user
# Подключаем модель юзера из моделей (для регистрации и логина), модель вопросов и базу данных
from . import db
from .models import Questions, User

# (https://flask.palletsprojects.com/en/1.1.x/tutorial/views/) либа для логинов и отслеживания того что юзер зашел
main = Blueprint('main', __name__)

# когда юзер переходит по этой ссылке в системе '/', то ему возвращается 'index.html' 
@main.route('/')
def index():
    return render_template('index.html')

# POST METHODS, POST это запрос на изменение данных, GET на получение
@main.route('/profile', methods=['GET', 'POST'])
# декоратор для проверки того что пользователь зашел в систему
@login_required
def profile():
    if request.method == 'GET':
        # Берем из базы данных вопросы которые относятся только к текущему юзеру
        uq = Questions.query.filter(Questions.user_questions.any(id=current_user.id)).all()
        # Собираем и возвращем 'profile.html' с нужными данными, которые обробатываются в джиндже 
        # https://jinja.palletsprojects.com/en/3.0.x/
        return render_template('profile.html', 
                                questions=uq, 
                                name=current_user.name, 
                                score=current_user.score,
                                role=current_user.role)

# POST METHODS, POST это запрос на изменение данных, GET на получение
@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_quest():
    # Если POST
    if request.method == 'POST':
        # Делаем исключение чтобы ничего не ломалось и админ увидел ошибку
        try:
            # Создаем новый тест на основе импортированной модели теста, вставляя в него данные из формы
            quest = Questions(request.form['title'], 
            request.form['text1'], request.form['answer1'],
            request.form['text2'], request.form['answer2'],
            request.form['text3'], request.form['answer3'],)

            # Добавляем в бд
            db.session.add(quest)
            # Получаем всех пользователй с бд
            users = User.query.all()
            # Для каждого юзера
            for user in users:
                # в связующую табличку добавляем тест
                user.user_questions.append(quest)
                db.session.add(user)
            # Отправляем в бд
            db.session.commit()
            # Кидаем на профиль
            return redirect('/profile')
        except Exception as e:
            # Если произошла какая-то ошибка то пишем ее на странице и в логах
            print(e)
            flash('Title is already in use')
            return redirect(url_for('main.add_quest'))
    # Если метод GET отдаем страницу, там производим проверку на роль, поэтому передаем еще и роль
    elif request.method == 'GET':
        return render_template('add_quest.html', role=current_user.role)

# Получение конкретного теста по айди
@main.route('/question/<id>/', methods=['GET'])
@login_required
def quest(id):
    if request.method == 'GET':
        # забираем тест из бд по айди
        quest = Questions.query.filter_by(id=id)
        # отдаем страничку с тестом
        return render_template('quest.html', question=quest)

# Удалаение конкретного теста по айди
@main.route('/delete', methods=['POST'])
@login_required
def delete_quest():
    # Забираем айди теста из формы отправки
    quest_id = request.form.get('id')
    # берем его из бд
    quest = Questions.query.filter_by(id=quest_id).first()
    # Удаляем
    db.session.delete(quest)
    # Сохраняем
    db.session.commit()
    # Кидаем на профиль
    return redirect(url_for('main.profile'))

# Проверка теста
@main.route('/check', methods=['POST'])
@login_required
def check():
    # Если пользователь адми, то просто уходим в профиль
    if current_user.role == 'admin':
        return redirect(url_for('main.profile'))
    
    # Собираем массив ответов пользователей
    quest_user_answers = [
        request.form['answer1'],
        request.form['answer2'],
        request.form['answer3']
    ]

    # Берем тест, на который отвечал пользователь
    quest = Questions.query.filter_by(id=request.form.get('id')).first()
    # Создаем массив с правильными ответами
    quest_answers = [
        quest.answer1,
        quest.answer2,
        quest.answer3,
    ]
    
    # Получаем массив правильно отвеченных ответов
    quest_right_answers = list(set(quest_answers) & set(quest_user_answers))
    # Кол-во правильных ответов
    score_new = len(quest_right_answers)
    # Берем пользователя из бд
    user = User.query.filter_by(id=current_user.id).first()
    # Берем текущие баллы пользователя
    score_old = current_user.score
    # Прибавляем новые баллы
    user.score = score_old + score_new*5

    # Этот запрос пришлось делать ручками через sql
    # Удаляем строчку из связующей таблицы
    sql = f"""DELETE FROM user_questions 
                WHERE user_id={current_user.id} 
                    AND question_id={request.form.get('id')}"""
    # Выполняем sql
    db.engine.execute(sql)
    # Сохраняем изменения
    db.session.commit()
    
    # Отдаем личный кабинет
    return redirect(url_for('main.profile'))
    
    
