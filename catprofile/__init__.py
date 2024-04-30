from flask import Flask
from .auth import auth

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "cat"

    from .catviews import catviews
    #from .auth import auth
    #from .catregister import catregister

    app.register_blueprint(catviews, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    #app.register_blueprint(catprofile, url_prefix='/catprofile')
    #app.register_blueprint(catregister, url_prefix='/catregister')


    return app