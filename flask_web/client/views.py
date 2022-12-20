from flask import Blueprint,render_template
from flask_login import current_user

views = Blueprint('views',__name__)

@views.route('/')
@views.route('/home')
def welcome():
    return render_template('index.html',user=current_user)

@views.route('/user')
def user():
    return render_template('user.html',user=current_user)

@views.route('/contact')
def contact():
    return 'contact page'

@views.route('/about')
def about():
    return 'about page'
