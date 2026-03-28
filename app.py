from flask import *
from models.user import *
from config import db
from models.user import bcrypt
from models.message import Message
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/projet_shadowcomm_bdd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bcrypt.init_app(app)
app.secret_key = 'e48a1b63d9196b0559f63564757e750697554f653457a419266736283c748261'

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        for key, val in request.form.items():
            if val == "":
                flash("aucun champ ne doit être vide",'error')
                return render_template('register.html')
        if re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", request.form.get('password')):
            User = Users.create_user(request.form.get('username'),request.form.get('password'))
            if User:
                return redirect(url_for('chat'))
            else:
                flash("error l'ore de la création de l'utilisateur en bdd non de code déjat utiliser","error")
                return render_template('register.html')
        else:
            flash("le mot de passe ne correspont pas au critére qui demander il faut aumoin 8 car. min, 1 maj, 1 chiffre, 1 cart.spécial (@$!%*?&)","error")
            return render_template('register.html')
    else:
        return render_template('register.html')
    
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        for key, val in request.form.items():
            if val == "":
                flash("aucun champ ne doit être vide","error")
                return redirect(url_for('index'),)
        if Users.log_user(request.form.get('username'),request.form.get('password')):
            return redirect(url_for('chat'))
        else:
            flash("mot de passe ou nom de code incorecte","error")
            return redirect(url_for('index'))


@app.route('/chat',methods=['GET', 'POST'])
def chat():
    if session.get('userID'):
        current_user = Users.getUser(session.get('userID'))
        if request.method == "POST" and request.form.get('message') !="":
            current_user.send_msg(request.form.get('message'))

        return render_template('chat.html', messages=Message.GetAllmsg(), current_user=None)
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    if session.get('userID'):
        user = Users.getUser(session.get('userID'))
        if user and user.deleateUser():
            session.clear()
            flash("les info de l'agent on bient été suprimer","success")
            return redirect(url_for('index'))
        else:
            flash("aucun agent enregister sous se non de code","error")
            return redirect(url_for('index'))
    else:
        flash("aucun agent n'est actuement connecter ","error")
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

