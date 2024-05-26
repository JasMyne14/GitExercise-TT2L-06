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
    
    from .models import User, Post, Comment

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)
                              )
    from .donation import donation
    from .notification import notification
    from .views import views
    from .user_posts import user_posts
    from .createpost import createpost
    from .signup import signup
    from .login import login
    from .mainpage import mainpage
    from .profile_page import profile_page
    from .registercat import registercat
    from .user import user
    from .adoptmeow import adoptmeow
    from .edit_profile import edit_profile

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(notification, url_prefix='/notification')
    app.register_blueprint(donation, url_prefix='/donation')
    app.register_blueprint(user_posts, url_prefix='/user_posts')
    app.register_blueprint(createpost, url_prefix='/createpost')
    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(signup, url_prefix='/signup')
    app.register_blueprint(mainpage, url_prefix='/mainpage')
    app.register_blueprint(profile_page, url_prefix='/profile_page')
    app.register_blueprint(registercat, url_prefix='/registercat')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(adoptmeow, url_prefix='/adoptmeow')
    app.register_blueprint(edit_profile, url_prefix='/edit_profile')


    return app