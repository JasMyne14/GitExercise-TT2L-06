from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import func
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'login'

def create_app():
    app = Flask(__name__,static_url_path='/static')
    app.config['SECRET_KEY'] = 'hwaiting'
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt = Bcrypt(app)

    login_manager = LoginManager()
    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .donation import donation
    from .notification import notification
    from .views import views
    from .post import post
    from .createpost import createpost
    from .signup import signup
    from .login import login
    from .mainpage import mainpage
    from .profile_page import profile_page
    from .registercat import registercat
    from .user import user
    from .adoptmeow import adoptmeow

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(notification, url_prefix='/notification')
    app.register_blueprint(donation, url_prefix='/donation')
    app.register_blueprint(post, url_prefix='/post')
    app.register_blueprint(createpost, url_prefix='/createpost')
    app.register_blueprint(login, url_prefix='/login')
    app.register_blueprint(signup, url_prefix='/signup')
    app.register_blueprint(mainpage, url_prefix='/mainpage')
    app.register_blueprint(profile_page, url_prefix='/profile_page')
    app.register_blueprint(registercat, url_prefix='/registercat')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(adoptmeow, url_prefix='/adoptmeow')



    return app
