from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "cat"

    from .catviews import viewscat
    #from .cat import profile_page
    #from .catregister import registercat

    app.register_blueprint(viewscat, url_prefix='/')
    #app.register_blueprint(profile_page, url_prefix='/catprofile')
    #app.register_blueprint(registercat, url_prefix='/catregister')
 
    return app