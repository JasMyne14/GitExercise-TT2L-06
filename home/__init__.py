from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = 'hwaiting'

    from .about_us import about
    from .notification import notification
    from .views import views


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(notification, url_prefix='/notification')
    app.register_blueprint(about, url_prefix='/about')

    return app