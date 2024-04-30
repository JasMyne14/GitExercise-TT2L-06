from flask import Blueprint

catviews = Blueprint('catviews', __name__)

@catviews.route('/')
def catprofile():
    return "<h1>Test</h1>"

#if __name__ == '__main__':
#    app.run(debug=True)