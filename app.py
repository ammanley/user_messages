from flask import Flask, render_template, url_for, redirect, request, flash
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf.csrf import CsrfProtect
from forms import NewForm, NewMessage

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/user_messages'
app.config['SECRET_KEY'] = 'shhhhhh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['TEMPLATES_AUTO_RELOAD'] = True
modus = Modus(app)
db = SQLAlchemy(app)
CsrfProtect(app)


@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/users/new')
def new():
    flash("Please fill in/correct the required fields")
    form = NewForm()
    return render_template('new.html', form=form)


@app.route('/users', methods = ['GET','POST'])
def index():
    form = NewForm(request.form)
    if request.method == 'GET':
        users = User.query.all()
        return render_template('index.html', users=users)
    if request.method == "POST" and form.validate():
        # flash("You have succesfully added a user!")
        db.session.add(User.new_for_form(form))
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == 'POST':
        return render_template('new.html', form=form)



@app.route('/users/<id>', methods = ['GET', 'PATCH', 'DELETE'])
def show(id):
    form = NewForm(request.form)
    user = User.query.filter_by(id = id).first()
    if request.method == b'PATCH':
        if form.validate():
            edit_user = User.new_for_form(form)
            user.username = edit_user.username
            user.email = edit_user.email 
            user.first_name =  edit_user.first_name
            user.last_name =  edit_user.last_name
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        else: 
            return render_template('edit.html', form=form , user=user)
    if request.method == b'DELETE':
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('index'))

    user = User.query.filter_by(id = id).first()
    return render_template('user.html', user=user)



@app.route('/users/<id>/edit')
def edit(id):

    user = User.query.filter_by(id = id).first()
    form = NewForm(obj = user)

    return render_template('edit.html', form=form, user=user)

######################

@app.route('/users/<id>/messages', methods = ['GET', 'POST'])
def show_msgs(id):

    if request.method == 'POST':

        db.session.add(Message(request.form['msg_text'], id))
        db.session.commit()


    messages = Message.query.filter_by(user_id = id)
    return render_template('index2.html', messages = messages, id=id)


@app.route('/users/<id>/messages/<msg_id>', methods=['DELETE','GET'])   
def msg_id(id, msg_id):

    if request.method == b'DELETE':
        # this isnt picking up the right IDs to find the message to delete
        message = Message.query.filter_by(id = msg_id).first()
        db.session.delete(message)
        db.session.commit()
        return render_template('message.html', id=id, msg_id = msg_id)


    messages = Message.query.filter_by(id = msg_id)
    return render_template('message.html', id=id, messages = messages, msg_id = msg_id)


@app.route('/users/<id>/messages/new')
def new_msg(id):
    msg = NewMessage()
    return render_template('new_msg.html', msg=msg, id=id)



@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

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
        # self.user_from = user_from


    def __repr__(self):
        return "Message Text: {}, Posted By: {}".format(self.msg_text, self.user.username)

db.create_all()
# from IPython import embed; embed()

if __name__ == '__main__':
    app.run(port=3000, debug=True)