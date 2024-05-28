from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'GURJAR Txt Bot 2'


if __name__ == "GURJAR Txt Bot 2":
    app.run()
