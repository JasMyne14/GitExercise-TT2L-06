from flask import Flask, Blueprint, render_template, request, redirect,url_for, flash, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from home import create_app
from .post import posts
from .forms import PostForm,SignUpForm,LoginForm, UpdateAccountForm
from .models import Post, User, RegisterCat, db
import bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os

views = Blueprint('views',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'appviews'


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
        hashed_password = generate_password_hash(form.password1.data)
        user = User(fullname=form.fullname.data,
                    email=form.email.data,
                    username=form.username.data,
                    password1=hashed_password,
                    password2=hashed_password,
                    state=form.selected_option.data,
                    phonenumber=form.phonenumber.data)
        db.session.add(user)
        db.session.commit()
        selected_option = form.selected_option.data
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('views.mainpage'))
    return render_template('signup.html', form=form)

@views.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.mainpage'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password1, form.password1.data):            
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('views.mainpage'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    return render_template('login.html', form=form)

@views.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('views.first'))

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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', 'picture_fn')
    form_picture.save(picture_path)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@views.route('/user', methods=['GET','POST'])
def user():
    return render_template('user.html')

@views.route('/adoptmeow')
def adoptmeow():
    return render_template('adoptmeow.html')