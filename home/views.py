from flask import Flask, Blueprint, render_template, request, redirect,url_for, flash, send_from_directory,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user
from .post import posts
from .forms import PostForm,SignUpForm,LoginForm
from .models import Post, User, RegisterCat
from flask_bcrypt import Bcrypt, generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
import os
from . import db

views = Blueprint('views',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'appviews'
app.config['UPLOAD_FOLDER'] = 'static/files'
bcrypt = Bcrypt()

@views.route('/')
def first():
    return render_template('firstpage.html', name='firstpage')

@views.route('/mainpage')
def mainpage():
    return render_template('mainpage.html', mainpage='mainpage', posts=posts)

@views.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.password1.data != form.password2.data:
            flash('password do not match','danger')
            return render_template('signup.html', form=form)
        
        hashed_password = generate_password_hash(form.password1.data).decode('utf-8')
        user = User(fullname=form.fullname.data, email=form.email.data, username=form.username.data, password1=hashed_password, password2=form.password2.data, selected_option = form.selected_option.data, phonenumber=form.phonenumber.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('views.mainpage'))
    return render_template('signup.html', form=form)

@views.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('try again')
        return redirect(url_for('views.login'))
    
    login_user(user, remember=remember)
    flash('You have been logged in!', 'success')
    return redirect(url_for('views.mainpage'))

@views.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully','info')
    return redirect(url_for('views.firstpage'))

@views.route('/notification')
def notification():
    users = {
        'user1': {'username': 'user1', 'notifications': []},
        'user2': {'username': 'user2', 'notifications': []}
    }    
    return render_template('notification.html', notification='Notification', users=users) 

@views.route('/post')
def post():
    return render_template('post.html', posts=posts)

@views.route('/createpost', methods=['GET','POST'])
def createpost():
    form = PostForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        flash('Your post has been created!','success')
        return redirect(url_for('views.mainpage'))
    return render_template('createpost.html', title='New Post', form=form,)
    
def adopt():
    return '<h2>Adoption page</h2>'

@views.route('/donation')
def donation():
    links= [{'url':"https://www.paws.org.my/donate", "text":"donate1"},
            {'url':"https://mnawf.org.my/donate/", "text":"donate2"},
            {'url':"https://catbeachpenang.com/donate/", "text":"donate3"}
    ]
    return render_template('donation.html', donation='donation', links=links)

@views.route('/registercat')
def registercat():
    return render_template('catregister.html') 

@views.route('/profile_page')
def profile_page():
    formcat = RegisterCat.query.all()
    return render_template('catprofile.html', formcat=formcat)

@views.route('/user')
def user():
    return render_template('user.html')

@views.route('/adoptmeow')
def adoptmeow():
    return render_template('adoptmeow.html')