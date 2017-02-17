from project import db

class User(db.Model):
    __tablename__ = 'users'
    # Why are these accesspible on the CLASS INSTANCE like __init__ properties
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text)
    email = db.Column(db.Text)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    messages = db.relationship('Message', backref = 'user', lazy='dynamic')

    @classmethod
    def new_for_form(cls,form):
        return User(form.username.data,
                    form.email.data,
                    form.first_name.data,
                    form.last_name.data)

    def __init__(self, username, email, first_name, last_name):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        

    def __repr__(self):
        return "ID: {}   Username: {}, Email: {}, First Name: {}, Last Name: {}".format(self.id, self.username, self.email, self.first_name,self.last_name)

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key = True)
    msg_text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self, msg_text, user_id):
        self.msg_text = msg_text
        self.user_id = user_id


    def __repr__(self):
        return "Message Text: {}, Posted By: {}".format(self.msg_text, self.user.username)


