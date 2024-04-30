from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#Secret key
app.config['SECRET_KEY'] = "find your treasure"
# Add this line to configure static file serving
app.static_folder = 'static'

#Initialize the database
db = SQLAlchemy(app)


#Create model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    #Create A String
    def __repr__(self):
        return 'Name %r>' % self.name
@app.route('/')
def index():
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        pass
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pass 
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
 