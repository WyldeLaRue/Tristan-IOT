from server import app
from flask import render_template

@app.route('/hello')
def hello_world():
    return 'Hello, World!'


@app.route('/')
def homepage():
	variable = 'FUCK'
	return render_template('homepage/templates/homepageTemplate.html', variable="FUCK")