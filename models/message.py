import datetime
from abc import *
from cesar import *
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import *
db = SQLAlchemy()

class Message(db.Model, ABC):
    __abstractmethods__ = True
    
    id = db.Column(db.Integer,primary_key= True)
    contente = db.Column(db.String(255), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    msg_date_time = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.relationship('User', backref=db.backref('messages', lazy=True))

    def send(msg):
        try:
            new_msg = Message(
                contente = chiffrer_cesar(msg),
                user = session['user_id']
            )
            db.session.add(new_msg)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False, str(e)