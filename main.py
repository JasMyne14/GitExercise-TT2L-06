from home import create_app
from home import db, bcrypt 

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)

