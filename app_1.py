from flask import Flask
#Creating a flask instance
app = Flask (__name__)
@app.route('/')
def hello_world():
    return "Hello world"

