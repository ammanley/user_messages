from flask_wtf.csrf import CsrfProtect
from flask import Flask, url_for, redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_modus import Modus
from flask_login import current_user, LoginManager
from flask_bcrypt import Bcrypt
from project.forms import NewForm
from functools import wraps

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/user_messages'
app.config['SECRET_KEY'] = 'shhhhhh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['TEMPLATES_AUTO_RELOAD'] = True
modus = Modus(app)
db = SQLAlchemy(app)
CsrfProtect(app)

login_manager.login_view = "users.login"
# This tells unlogged in users where to go

from project.users.views import users_blueprint
from project.messages.views import messages_blueprint
from project.models import User

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(messages_blueprint, url_prefix='/users/<int:id>/messages')

@app.route('/')
def root():
	return redirect(url_for('users.login'))

def ensure_current_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user != User.query.get(kwargs.get('id')):
            flash("You are not authorized to access this page.")
            return redirect(url_for('users.index'))
        return fn(*args, **kwargs)
    return wrapper