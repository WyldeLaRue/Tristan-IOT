from server import app, testObject
import server.lights as lights
import server.patterns as patterns
from server.patterns import rgbColor, hsvColor
from flask import render_template, request
import subprocess
from server.tests import debugMain

@app.route('/hello')
def hello_world():
    testObject.color = "blue"
    testObject.value += 1
    print("hello")
    return 'Hello, World!'

@app.route('/start')
def start():
    pass
    return "Created thread"

@app.route('/')
def homepage():
    variable = "ayy lmao"
    return render_template('homepage/templates/homepageTemplate.html', variable=variable)

@app.route('/debug')
def debugPage():
    print('DEBUGGING:')
    debugMain()


@app.route('/api/lights/setPattern/<pattern>')
def setPattern(pattern):
    return lights.addPattern(pattern)

@app.route('/api/lights/setAttribute', methods=['POST'])
def setAttribute():
    if request.method == 'POST':
        value = request.form['value']
        attribute = request.form['attribute']
        if attribute == "brightness":
            lc.setBrightness(float(value))
        elif attribute == "speed":
            lc.setSpeed(float(value))
        return "success"

@app.route('/api/outlets/toggle', methods=['POST'])
def manageOutlets():
    print('test')
    if request.method == 'POST':
        outletId = request.form['outletId']
        state = request.form['state']
        freqON = {  '1': 87347,
                    '2': 87491,
                    '3': 87811,
                    '4': 89347,
                    '5': 95491}
        freqOFF = { '1': 87356,
                    '2': 87500,
                    '3': 87820,
                    '4': 89356,
                    '5': 95500}
        if state == "ON":
            signature = freqON[outletId]
            print(("Turning on " + outletId))
            subprocess.call(('/var/www/rfoutlet/codesend %d -l 180 -p 0' % signature), shell=True)
            return "toggle success"
        else:
            signature = freqOFF[outletId]
            print(("Turning off " + outletId))
            subprocess.call(('/var/www/rfoutlet/codesend %d -l 180 -p 0' % signature), shell=True)
            return "toggle success"
