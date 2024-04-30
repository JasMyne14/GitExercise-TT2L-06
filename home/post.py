from flask import Flask,Blueprint,render_template,redirect,request, url_for
from flask_sqlalchemy import SQLAlchemy

post = Blueprint('post',__name__)

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'form'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@post.route('/post/new',methods=['GET','POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('main'))
    
    return render_template('post.html')