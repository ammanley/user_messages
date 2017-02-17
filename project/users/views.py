from flask import Flask, render_template, url_for, redirect, request, flash, Blueprint
from flask_wtf.csrf import CsrfProtect
from project.forms import NewForm, NewMessage
from sqlalchemy.exc import IntegrityError
from functools import wraps
from project import app, db

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates/users'
)


@users_blueprint.route('/')
def root():
    return redirect(url_for('index'))

@users_blueprint.route('/users/new')
def new():
    flash("Please fill in/correct the required fields")
    form = NewForm()
    return render_template('new.html', form=form)


@users_blueprint.route('/users', methods = ['GET','POST'])
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



@users_blueprint.route('/users/<id>', methods = ['GET', 'PATCH', 'DELETE'])
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



@users_blueprint.route('/users/<id>/edit')
def edit(id):

    user = User.query.filter_by(id = id).first()
    form = NewForm(obj = user)

    return render_template('edit.html', form=form, user=user)


