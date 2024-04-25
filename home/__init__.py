from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = 'hwaiting'

    from .notification import notification
    from .views import views
    from .about_us import about_us

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(about_us, url_prefix='/about_us')
    app.register_blueprint(notification, url_prefix='/notification')


    return app