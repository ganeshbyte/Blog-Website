from flask import Blueprint, make_response, redirect, render_template, url_for,flash
from flask_login import current_user, login_user, logout_user
from .forms import RegistrationForm,LoginForm
from flasknotes import db,bcrypt
from flasknotes.models import User


# Defining a blueprint
auth = Blueprint(
    'auth', __name__,
    template_folder='templates',
    static_folder='static',url_prefix="/login"
)


@auth.route("/register", methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return make_response(redirect(url_for('home')))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return make_response(redirect(url_for('auth.login')))

    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash( f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', title='Register', form=form)

@auth.route("/login",methods=['POST','GET'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('login.html', form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

