from flask_wtf.csrf import CsrfProtect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_modus import Modus
from flask_login import current_user, LoginManager
from flask_bcrypt import Bcrypt

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

from project.models import User, Message
from project.users.views import users_blueprint
from project.messages.views import messages_blueprint

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(messages_blueprint, url_prefix='/users<int:id>/messages')