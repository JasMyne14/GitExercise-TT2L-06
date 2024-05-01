from flask import Blueprint

viewscat = Blueprint('catviews', __name__)

@viewscat.route('/')
def viewscat():
    return "<h1>Test</h1>"

if __name__ == '__main__':
  app.run(debug=True)