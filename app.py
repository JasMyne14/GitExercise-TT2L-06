from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Add this line to configure static file serving
app.static_folder = 'static'

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
