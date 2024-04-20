from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = 'hwaiting'

    from .notification import notification
    from .views import views
    
    app.register_blueprint(notification, url_prefix='/notification')
    app.register_blueprint(views, url_prefix='/')

    return app