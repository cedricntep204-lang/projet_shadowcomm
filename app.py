from flask import *
from models.user import *;
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/projet_shadowcomm_bdd'
db.init_app(app)
@app.route('/')
def home():
    success = Users.create_user("cO3","hello")
    if success:
        return render_template("index.html")
    else:
        return "Erreur lors de la création."
