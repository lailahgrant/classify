from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from project import db, bcrypt
# from project.models import User, Bplan
# from project.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
#                                    RequestResetForm, ResetPasswordForm)
# from project.users.utils import  send_reset_email ,save_picture
# from werkzeug.urls import url_parse

users = Blueprint('users', __name__)

@users.route('/')
def show_login_signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('login.html')


@users.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        data = request.form
        existing_user = User.query.filter(User.email==data['email']).first()###
        if existing_user:
            flash('User with given email address already exists, please Login or Signup with different email', 'error')
            return redirect(request.referrer) 
        new_user = User(email = data['email'],
                        username = data['username'],
                        password = User.hash_password(data['password']),
                    )
        new_user.save()
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home')
        return redirect(next_page)
    else:
        return render_template('register.html')



@users.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        data = request.form
        email = data['email']
        password = data['password']
        remember = True if request.form.get('remember_me') else False
        user = User.query.filter(User.email==email).first()###
        if not user:
            flash("Account doesn't exist",'error')
            return redirect(request.referrer)
        if not user.is_password_valid(password):
            flash('Login Unsuccessful. Please check email and password', 'error')
            return redirect(request.referrer)
        login_user(user, remember=remember)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home')
        return redirect(next_page)
    else:
        return render_template('login.html')


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


# @users.route("/user/<string:username>")
# def user_bplans(username):
#     page = request.args.get('page', 1, type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     bplans = Bplan.query.filter_by(author=user)\
#         .order_by(Bplan.date_posted.desc())\
#         .paginate(page=page, per_page=5)
#     return render_template('user_bplans.html', bplans=bplans, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)