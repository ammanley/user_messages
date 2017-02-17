from flask import Flask, render_template, url_for, redirect, request, flash, Blueprint
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy 
from flask_wtf.csrf import CsrfProtect
from project.forms import NewForm, NewMessage
from sqlalchemy.exc import IntegrityError
from functools import wraps
from project import app,db

messages_blueprint = Blueprint(
    'messages',
    __name__,
    template_folder='templates/messages'
)

@messages_blueprint.route('/users/<id>/messages', methods = ['GET', 'POST'])
def show_msgs(id):

    if request.method == 'POST':

        db.session.add(Message(request.form['msg_text'], id))
        db.session.commit()


    messages = Message.query.filter_by(user_id = id)
    return render_template('index2.html', messages = messages, id=id)


@messages_blueprint.route('/users/<id>/messages/<msg_id>', methods=['DELETE','GET'])   
def msg_id(id, msg_id):

    if request.method == b'DELETE':
        # this isnt picking up the right IDs to find the message to delete
        message = Message.query.filter_by(id = msg_id).first()
        db.session.delete(message)
        db.session.commit()
        return render_template('message.html', id=id, msg_id = msg_id)


    messages = Message.query.filter_by(id = msg_id)
    return render_template('message.html', id=id, messages = messages, msg_id = msg_id)


@messages_blueprint.route('/users/<id>/messages/new')
def new_msg(id):
    msg = NewMessage()
    return render_template('new_msg.html', msg=msg, id=id)


