from flask import (Flask, g, render_template, flash, redirect, url_for, abort)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                        login_required, current_user)

import forms
import models

DEBUG = True
PORT = 8000 # use "localhost:8000" in browser to see app
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'jhvkhxxese64bkkm,bh;cxzezfugojljl.niugyf'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' #if not logged in redirect to login page

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist: # from peewee
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.get_conn()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST')) #allows for loading and filling out form
def register():
    form = forms.RegisterForm() # flask knows to use the imput from the user
    if form.validate_on_submit():
        flash("Registration Complete!", "success")
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user) #creates a session with a cookie containing user information
                flash("Login Successful!", "success")
                return redirect(url_for('taco'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout(): #delets cookie created by login()
    logout_user()
    flash("Logout Successful! Come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/taco', methods=('GET', 'POST'))
@login_required
def taco():
    form = forms.TacoForm()
    if form.validate_on_submit():
        models.Taco.create(user=g.user._get_current_object(),
         protein=form.protein.data,
         shell=form.shell.data,
         cheese=form.cheese.data,
         extras=form.extras.data
        )
        flash("Taco created!", "success")
        return redirect(url_for('index'))
    return render_template('taco.html', form=form)


@app.route('/')
def index():
    tacos = models.Taco.select().limit(100)
    return render_template('index.html', tacos=tacos)


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            email='leighd2008@gmail.com',
            password='1hgielenaid1',
            admin=True
        )
    except ValueError:
        pass


    app.run(debug=DEBUG, host=HOST, port=PORT)
