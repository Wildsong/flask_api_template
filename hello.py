import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    msg = ''
    for item in os.environ.items():
        msg += f"{item[0]} : {item[1]} <br/>"
    return "<h1>Hello World!</h1>" + msg

