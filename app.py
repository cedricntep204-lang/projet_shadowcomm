from flask import *
from models.user import *
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
                return render_template('chat.html')
            else:
                return render_template('index.html')
        else:
            return render_template('register.html')
    else:
        print(session.get("user_id"))
        return render_template('register.html')
    
@app.route('/login',methods=['GET', 'POST'])
def login():
    return ''

@app.route('/chat',methods=['GET', 'POST'])
def chat():
    return render_template('chat.html', messages=[], current_user=None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)