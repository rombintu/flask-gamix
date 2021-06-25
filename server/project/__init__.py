import os
# https://flask.palletsprojects.com/en/2.0.x/
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    
    # app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    # """После создания таблиц в базе данных, 
    # можно раскомментить строчку выше и 
    # закомментить которая ниже, чтобы брать переменную из окружения"""
    app.config['SECRET_KEY'] = 'insert-your-secret'
    # без этой строчки вылетают предупреждения, там и написано ее включить
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # следующие две строчки для свича бд, если нужна postgres, расскомментить
    # app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://test:password@localhost:5432/gamix"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # Инициализация приложения
    db.init_app(app)

    # https://flask-login.readthedocs.io/en/latest/
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Импорт модели юзера для отслеживания входа в систему
    from .models import User


    # Подключение blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    @login_manager.user_loader
    def load_user(user_id):
        """id - Первичный ключ, 
        поэтому используем его
        для управления авторизации"""
        return User.query.get(int(user_id))
    return app