from flask import Flask, Blueprint, render_template, request, redirect,url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from home import create_app
from .post import posts
from .forms import PostForm,RegistrationForm,LoginForm
from .models import Post

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.user.data}!','success')
        return redirect(url_for('mainpage'))
    return render_template('signup.html', title='Sign Up', form=form)

@views.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='login', form=form)

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