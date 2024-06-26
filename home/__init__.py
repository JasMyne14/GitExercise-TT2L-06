from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import func
from .forms import PostForm,SignUpForm,LoginForm
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager = LoginManager()
login_manager.login_view = 'views.login'

def create_app():
    app = Flask(__name__,static_url_path='/static')
    app.config['SECRET_KEY'] = 'hwaiting'
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'views.login'
    login_manager.login_message_category = 'info'
    
    from .models import User, Post, Comment, Notification, AdoptionNotification

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .donation import donation
    from .notification import notification
    from .views import views
    from .user_posts import user_posts
    from .createpost import createpost
    from .signup import signup
    from .login import login
    from .mainpage import mainpage
    from .catprofile import catprofile
    from .registercat import registercat
    from .userprofile import userprofile
    from .adoptmeow import adoptmeow
    from .user_edit import user_edit
    from .profiledisplay import profiledisplay
    from .otheruser_post import otheruser_post

    #register blueprint
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(notification, url_prefix='/notification')
    app.register_blueprint(donation, url_prefix='/donation')
    app.register_blueprint(user_posts, url_prefix='/user_posts')
    app.register_blueprint(createpost, url_prefix='/createpost')
    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(signup, url_prefix='/signup')
    app.register_blueprint(mainpage, url_prefix='/mainpage')
    app.register_blueprint(catprofile, url_prefix='/catprofile')
    app.register_blueprint(registercat, url_prefix='/registercat')
    app.register_blueprint(userprofile, url_prefix='/userprofile')
    app.register_blueprint(adoptmeow, url_prefix='/adoptmeow')
    app.register_blueprint(user_edit, url_prefix='/user_edit')
    app.register_blueprint(profiledisplay, url_prefix='/profiledisplay')
    app.register_blueprint(otheruser_post, url_prefix='/otheruser_post')

    return app