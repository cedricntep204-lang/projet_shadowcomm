from flask import *
from abc import ABC, abstractmethod
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import *
db = SQLAlchemy()
class Users(db.Model, ABC):
    __abstractmethods__ = True
    
    id = db.Column(db.Integer,primary_key= True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    @staticmethod
    def create_user(name,mdp):
        try:
            mdp = Bcrypt.generate_password_hash(mdp).decode('utf-8')
            newUser = Users(username=name,password=mdp)
            db.session.add(newUser)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"erreur BDD: {e}")
            return False
        
    def log_user(name,mdp):
        User = Users.query.filter_by(username=name,password=mdp)
        if User and check_password_hash(User.password, mdp):
            session['user_id'] = User.id
            session['username'] = User.username
            return True
        else:
            return False
        
    def send_msg():
        from message import send
        send()

    def __repr__(self):
        return f"<User {self.username}"