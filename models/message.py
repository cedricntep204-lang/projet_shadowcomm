import datetime
from cesar import *
from flask import *
from config import db
from flask_bcrypt import *


class Message(db.Model):
    
    __tablename__ = 'chat'

    id = db.Column(db.Integer,primary_key= True)
    contente = db.Column(db.String(255), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    msg_date_time = db.Column(db.DateTime, default=False)
    author = db.relationship('Users', backref=db.backref('messages', lazy=True))

    @staticmethod
    def insert_msg_in_bdd(sender_id,msg):
        try:
            new_msg = Message(
                contente = chiffrer_cesar(msg,10),
                user = sender_id,
                msg_date_time = datetime.datetime.now()
            )
            db.session.add(new_msg)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"ERREUR BDD MESSAGE: {e}")
            return False,

    def GetAllmsg():
        try:
            allmsg = Message.query.order_by(Message.msg_date_time.asc())
            for i in allmsg:
                contente = i.contente
                i.contente = dechiffrer_cesar(contente)
            return allmsg
        except Exception as e:
            db.session.rollback()
            print(f"ERREUR BDD MESSAGE: {e}")
            return False,
