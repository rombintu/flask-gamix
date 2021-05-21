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
        questions = Questions.query.all()
        return render_template('profile.html', 
                                questions=questions, 
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
        
# ДОПИЛ
@main.route('/check', methods=['POST'])
@login_required
def check():
    quest_user = [
        request.form['text1'], request.form['answer1'],
        request.form['text2'], request.form['answer2'],
        request.form['text3'], request.form['answer3']
    ]

    quest = Questions.query.filter_by(id=id).first()
    
    
