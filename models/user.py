from flask_sqlalchemy import SQLAlchemy;
db = SQLAlchemy()
class Users(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    @staticmethod
    def create_user(name,mdp):
        try:
            newUser = Users(username=name,password=mdp)
            db.session.add(newUser)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"erreur BDD: {e}")
            return False

    def __repr__(self):
        return f"<User {self.username}"