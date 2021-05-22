from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from . import db
from .models import Questions, User
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'GET':
        uq = Questions.query.filter(Questions.user_questions.any(id=current_user.id)).all()

        return render_template('profile.html', 
                                questions=uq, 
                                name=current_user.name, 
                                score=current_user.score,
                                role=current_user.role)


@main.route('/add', methods=['GET', 'POST'])
@login_required
def add_quest():
    if request.method == 'POST':
        try:
            quest = Questions(request.form['title'], 
            request.form['text1'], request.form['answer1'],
            request.form['text2'], request.form['answer2'],
            request.form['text3'], request.form['answer3'],)

            db.session.add(quest)

            users = User.query.all()

            for user in users:
                user.user_questions.append(quest)
                db.session.add(user)
            db.session.commit()
            return redirect('/profile')
        except Exception as e:
            print(e)
            flash('Title is already in use')
            return redirect(url_for('main.add_quest'))

    elif request.method == 'GET':
        return render_template('add_quest.html', role=current_user.role)


@main.route('/question/<id>/', methods=['GET'])
@login_required
def quest(id):
    if request.method == 'GET':
        quest = Questions.query.filter_by(id=id)
        return render_template('quest.html', question=quest)
        
@main.route('/delete', methods=['POST'])
@login_required
def delete_quest():
    quest_id = request.form.get('id')
    quest = Questions.query.filter_by(id=quest_id).first()
    db.session.delete(quest)
    db.session.commit()
    
    return redirect(url_for('main.profile'))

@main.route('/check', methods=['POST'])
@login_required
def check():
    if current_user.role == 'admin':
        return redirect(url_for('main.profile'))
    quest_user_answers = [
        request.form['answer1'],
        request.form['answer2'],
        request.form['answer3']
    ]

    quest = Questions.query.filter_by(id=request.form.get('id')).first()
    quest_answers = [
        quest.answer1,
        quest.answer2,
        quest.answer3,
    ]
    
    quest_right_answers = list(set(quest_answers) & set(quest_user_answers))
    
    score_new = len(quest_right_answers)
    user = User.query.filter_by(id=current_user.id).first()
    score_old = current_user.score
    user.score = score_old + score_new*5
    print(quest_right_answers)

    sql = f"""DELETE FROM user_questions 
                WHERE user_id={current_user.id} 
                    AND question_id={request.form.get('id')}"""
    db.engine.execute(sql)
    db.session.commit()
    

    return redirect(url_for('main.profile'))
    
    
