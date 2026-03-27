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
                return render_template('register.html')
        if re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", request.form.get('password')):
            User = Users.create_user(request.form.get('username'),request.form.get('password'))
            if User:
                return redirect(url_for('chat'))
            else:
                return redirect(url_for('index'))
        else:
            return render_template('register.html')
    else:
        return render_template('register.html')
    
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        for key, val in request.form.items():
            if val == "":
                return redirect(url_for('index'))
        if Users.log_user(request.form.get('username'),request.form.get('password')):
            return redirect(url_for('chat'))
        else:
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

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)