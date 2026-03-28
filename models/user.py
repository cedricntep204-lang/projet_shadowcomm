from flask import *
from flask_bcrypt import *
from config import db
bcrypt = Bcrypt()
class Users(db.Model):
    
    id = db.Column(db.Integer,primary_key= True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    @staticmethod
    def create_user(name,mdp):
        
        try:
            user = Users.query.filter_by(username=name).first()
            if user:
                return False
            else:
                mdp = bcrypt.generate_password_hash(mdp).decode('utf-8')
                newUser = Users(username=name,password=mdp)
                db.session.add(newUser)
                db.session.commit()
                session['userID'] = newUser.id
                return True
        except Exception as e:
            db.session.rollback()
            print(f"erreur BDD: {e}")
            return False

    @staticmethod
    def log_user(name,mdp):
        User = Users.query.filter_by(username=name).first()
        if User and check_password_hash(User.password, mdp):
            session['userID'] = User.id
            return True
        else:
            return False
        
    @staticmethod
    def getUser(user_id):
    # .get() est la méthode la plus rapide pour chercher par l'ID (clé primaire)
        return Users.query.get(int(user_id))
    
    def deleateUser(self):
        try:
            db.session.delete(self)
            db.session.commit()
            session.clear()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"erreur BDD: {e}")
            return False

    
    def send_msg(self,msg_content):
        from models.message import Message
        return Message.insert_msg_in_bdd(sender_id=self.id,msg=msg_content)

    def __repr__(self):
        return f"<User {self.username}"