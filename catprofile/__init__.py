from flask import Flask,Blueprint

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "cat"

    from .viewscat import viewscat
    from .profile_page import profile_page
    from .registercat import registercat

    app.register_blueprint(viewscat, url_prefix='/')
    app.register_blueprint(profile_page, url_prefix='/profile_page')
    app.register_blueprint(registercat, url_prefix='/registercat')
 
    return app