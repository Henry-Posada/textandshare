# Imports
from flask_socketio import SocketIO, send, emit
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Initializations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Henry/Desktop/School/textandshare/db/database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Creates User class for database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login page form
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

# Sign up page form
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

# Index page route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home', methods=['POST'])
def home():
	return render_template("index.html")

# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Authenticate user
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('session'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)

# Sign up page route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'

    return render_template('signup.html', form=form)

# Session page route
@app.route('/session')
#@login_required
def session():
    return render_template('session.html', name=current_user.username)

# Log out route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Socket IO 
socketio = SocketIO(app, cors_allowed_origins="*")
clients = 0
message = ""

@socketio.on('connect')
def connect():
    global clients
    clients += 1
    emit("users", {"user_count": clients, "message" : message}, broadcast = True)

@socketio.on('disconnect')
def disconnect():
    global clients
    clients -=1
    emit("users", {"user_count": clients, "message" : message}, broadcast= True)

@socketio.on('message')
def handleMessage(msg):
    #print('Message: ' + str(msg))
    global message
    message = msg
    send(msg, broadcast=True) #broadcasting received message to all connect clients, including the one that sent it.

if __name__ == '__main__':
    socketio.run(app, debug=True)