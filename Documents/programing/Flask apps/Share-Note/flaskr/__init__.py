from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from os import path

db = SQLAlchemy()


def create_app():
    app = Flask(__name__) 
    app.config['SECRET_KEY'] = 'huiok'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///note.db' 
    # db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    db.init_app(app)

    from .view import view
    from .up import up
    from .update import update
    from .auth import auth

    app.register_blueprint(view)
    app.register_blueprint(up)
    app.register_blueprint(update)
    app.register_blueprint(auth)

    from .models import Note
    from .models import User

    # db.create_all(app=app)
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/'+'note.db'):
        db.create_all(app=app)
        print('Cteated database!')