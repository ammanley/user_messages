from flask_wtf import FlaskForm
from wtforms import StringField, validators

class NewForm(FlaskForm):
	username = StringField('Username', [validators.Length(min=5)])
	email = StringField('Email', [validators.Email()])
	first_name = StringField('First Name', [validators.InputRequired()])
	last_name = StringField('Last Name', [validators.InputRequired()])

class NewMessage(FlaskForm):
	# user_id = IntegerField('User ID', [validators.InputRequired()])
	msg_text = StringField('Message', [validators.InputRequired()])
