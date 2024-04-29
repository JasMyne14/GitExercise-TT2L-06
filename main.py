from home import create_app,Flask

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)