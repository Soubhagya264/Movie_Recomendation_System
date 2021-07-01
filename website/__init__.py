from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


from os import path

db=SQLAlchemy()
DB_Name="database.db"

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']="thisismysecretkey"
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_Name}'
    db.init_app(app)
    login_manager=LoginManager()
    login_manager.login_view='login'
    login_manager.init_app(app)
    from .models import User
    create_database(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    
    return app
def create_database(app):
    if not path.exists('website/'+DB_Name):
        db.create_all(app=app)
        print("Created Database!")