from server import app, testObject
from server.LightController import lc
from flask import render_template

@app.route('/hello')
def hello_world():
    testObject.color = "blue"
    testObject.value += 1
    print "hello"
    return 'Hello, World!'


@app.route('/')
def homepage():
    lc.createThread()
    testObject.info()
    variable = "debug"
    return render_template('homepage/templates/homepageTemplate.html', variable=variable)