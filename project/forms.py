from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class NewForm(FlaskForm):
	username = StringField('Username', [validators.Length(min=5)])
	password = PasswordField('Password', [validators.InputRequired()])
	email = StringField('Email', [validators.Email()])
	first_name = StringField('First Name', [validators.InputRequired()])
	last_name = StringField('Last Name', [validators.InputRequired()])

class NewMessage(FlaskForm):
	# user_id = IntegerField('User ID', [validators.InputRequired()])
	msg_text = StringField('Message', [validators.InputRequired()])

class LoginForm(FlaskForm):
	username = StringField('Username', [validators.InputRequired()])
	password = PasswordField('Password', [validators.DataRequired()])