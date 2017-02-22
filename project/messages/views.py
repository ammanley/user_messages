from flask import Flask, render_template, url_for, redirect, request, flash, Blueprint
# from flask_sqlalchemy import SQLAlchemy 
# from flask_wtf.csrf import CsrfProtect
from project.forms import NewMessage
# from sqlalchemy.exc import IntegrityError
from functools import wraps
from project import db
from project.models import Message, User
from flask_login import  current_user, login_required, login_user, logout_user

messages_blueprint = Blueprint(
    'messages',
    __name__,
    template_folder='templates'
)

def ensure_current_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user != User.query.get(kwargs.get('id')):
            flash("You are not authorized to access this page.")
            return redirect(url_for('users.index'))
        return fn(*args, **kwargs)
    return wrapper

@messages_blueprint.route('/', methods = ['GET', 'POST'])
@login_required
def show(id):
    if request.method == 'POST':
        db.session.add(Message(request.form['msg_text'], id))
        db.session.commit()
    messages = Message.query.filter_by(user_id = id)
    user = User.query.filter_by(id=id).first()
    return render_template('messages/message.html', messages = messages, id=id, user=user)

@messages_blueprint.route('/<int:msg_id>/edit')
@login_required
@ensure_current_user
def edit(id, msg_id):
    user = User.query.filter_by(id=id).first()
    message = Message.query.filter_by(id = msg_id).first()
    form = NewMessage(obj=message)
    return render_template('messages/edit.html', id=id, msg_id=msg_id, form=form, user=user)


@messages_blueprint.route('/<int:msg_id>', methods=['DELETE','GET', 'PATCH'])   
@login_required
@ensure_current_user
def msg_id(id, msg_id):
    user = User.query.filter_by(id=id).first()
    messages = Message.query.filter_by(id = msg_id).first()
    if request.method == b'DELETE':
        message = Message.query.filter_by(id = msg_id).first()
        db.session.delete(message)
        db.session.commit()
        flash("Message deleted.")
        # return render_template('messages/message.html', id=id, msg_id = msg_id, user=user, messages=messages)
        return redirect(url_for('messages.show', id=id, msg_id=msg_id))
    if request.method == b'PATCH':
        form = NewMessage(request.form)
        if form.validate():
            messages.msg_text = form['msg_text'].data
            db.session.add(messages)
            db.session.commit()
            flash('Message edited.')
            messages = Message.query.filter_by(user_id = id)
            return render_template('messages/message.html', id=id, messages = messages, msg_id = msg_id, user=user)
        flash("Data required to submit edits.")
        return redirect(url_for('messages.edit', id=id, msg_id=msg_id))

    return render_template('messages/message.html', id=id, messages = messages, msg_id = msg_id, user=user)


@messages_blueprint.route('/new')
@login_required
@ensure_current_user
def new(id):
    msg = NewMessage()
    return render_template('messages/new.html', msg=msg, id=id)




@messages_blueprint.app_errorhandler(404)
def page_not_found(e):
    flash ("YOU BROKE MESSAGES!")
    return "YOU BROKE MESSAGES!", 404