from flask import Flask, jsonify,request,render_template,session,json,redirect,url_for



## Creating a object of the class and initialization of parameterized flask constructor
app=Flask(__name__)


## HTTP GET (R- READ) method call and showing the welcome page for the app


@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')


## run the flask application
if (__name__)==('__main__'):
    app.run(host="127.0.0.1",port='3001')