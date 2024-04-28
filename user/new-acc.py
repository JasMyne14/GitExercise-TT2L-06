from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask('__name__')
app.secret_key = 'new-account'

#MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'flask_users'

mysql = MySQL(app)

@app.route('/')
def home():
    if 'username' in sessions:
        return render_template('homepage.html', username=session['username'])
    else:
        return render_template('homepage.html')

@app.route('/')
def login():
    if request.method == 'POST':
        username = request.form
