from flask import Flask

def create_app():
    app = Flask(__name__)
    app.confiq['SECRET KEY'] = 'none'
    
    return app

