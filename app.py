from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')





@app.route('/register')
def register():
    return render_template('register.html')





@app.route('/chat')
def chat():
    return render_template('chat.html', messages=[], current_user=None)

if __name__ == '__main__':
    app.run(debug=True)





if __name__ == '__main__':
    app.run(debug=True)