from flask import Flask, render_template, url_for, redirect, request, flash, Blueprint
from flask_wtf.csrf import CsrfProtect
from project.forms import NewForm, NewMessage, LoginForm
from sqlalchemy.exc import IntegrityError
from functools import wraps
from project import app, db, bcrypt
from project.models import User
from flask_login import  current_user, login_required, login_user, logout_user


users_blueprint = Blueprint(
    'users',
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

@users_blueprint.route('/', methods = ['GET','POST'])
# @login_required
def index():
    form = NewForm(request.form)
    if request.method == 'GET':
        users = User.query.all()
        return render_template('users/index.html', users=users)
    # if request.method == "POST":
    #     if form.validate():
    #         flash("You have succesfully added a user!")
    #         db.session.add(User.new_for_form(form))
    #         db.session.commit()
    #         return redirect(url_for('users.index'))
    #     flash("Please fill in/correct the required fields")
    #     return render_template('users/signup.html', form=form)



@users_blueprint.route('/<id>', methods = ['GET', 'PATCH', 'DELETE'])
@login_required
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
            return redirect(url_for('users.index'))
        else: 
            return render_template('users/edit.html', form=form , user=user)
    if request.method == b'DELETE':
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('users.index'))

    user = User.query.filter_by(id = id).first()
    return render_template('users/user.html', user=user, id=id)



@users_blueprint.route('/<id>/edit')
@login_required
@ensure_current_user
def edit(id):
    user = User.query.filter_by(id = id).first()
    form = NewForm(obj = user)
    return render_template('users/edit.html', form=form, user=user)


@users_blueprint.route('/signup', methods=['GET',"POST"])
def signup():
    form = NewForm(request.form)
    if request.method == 'POST':
        if form.validate():
            flash("You have succesfully created an account.")
            db.session.add(User.new_for_form(form))
            db.session.commit()
            return redirect(url_for('users.index'))
        flash("Please fill in/correct the required fields")
        return render_template('users/signup.html', form=form)
    return render_template('users/signup.html', form=form)
######################### Check for unique user ID

@users_blueprint.route('/login', methods = ["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        if form.validate():
            found_user = User.query.filter_by(username=form.username.data).first()
            if found_user:
                authenticated_user = bcrypt.check_password_hash(found_user.password, form.password.data)
                if authenticated_user:
                    login_user(found_user)
                    flash("You have been logged in!")
                    return redirect(url_for('users.index'))

######################### check password
# Set session
            flash("Invalid credentials")    
            return redirect(url_for('users.login'))
        return render_template('users/login.html', form=form)
    return render_template('users/login.html', form=form)


@users_blueprint.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('users.login'))


@users_blueprint.app_errorhandler(404)
def page_not_found(e):
    flash("YOU ARE IN THE WRONG PLACE!")
    return render_template('index.html'), 404

