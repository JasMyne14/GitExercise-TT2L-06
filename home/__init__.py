from flask import Flask

def create_app():
    app = Flask(__name__,static_url_path='/static')
    app.config['SECRET KEY'] = 'hwaiting'

    from .donation import donation
    from .notification import notification
    from .views import views
    from .post import post


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(notification, url_prefix='/notification')
    app.register_blueprint(donation, url_prefix='/donation')
    app.register_blueprint(post, url_prefix='/post')


    return app