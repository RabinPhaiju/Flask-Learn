from flask import Blueprint,render_template,request,flash,redirect,url_for
from werkzeug.utils import redirect
from .models import User
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user
from flask_login import current_user

auth = Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password,password):
            flash('Email or password do not match',category='error')
        else:
            flash('Login Successful.',category='success')

            login_user(user,remember=True)
            return redirect(url_for('todos.todo'))
    return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.welcome'))

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if len(email)<4:
            flash('Email must be greater than 4 characters',category='error')
        elif len(firstname)<2:
            flash('Firstname must be greater tha 3 character',category='error')
        elif password2!=password1:
            flash('Password dont match',category='error')
        elif len(password1)<7:
            flash('Password must be greater tha 6 character',category='error')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('Email already taken!',category='error')
            else:
                user = User(email=email,firstname=firstname,lastname=lastname,password=generate_password_hash(password1))
                db.session.add(user)
                db.session.commit()
                flash('Account Created',category='success')
                return redirect(url_for('auth.login'))
    return render_template('signup.html',user=current_user)