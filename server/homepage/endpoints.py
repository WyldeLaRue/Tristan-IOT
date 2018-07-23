from server import app, testObject
import server.lights as lights
from server.alarm import alarm
import server.patterns as patterns
from flask import render_template, request
import subprocess
from server.tests import debugMain

@app.route('/hello')
def hello_world():
    testObject.color = "blue"
    testObject.value += 1
    print("hello")
    return "success"

@app.route('/start')
def start():
    pass
    return "success"

@app.route('/')
def homepage():
    variable = "ayy lmao"
    return render_template('homepage/templates/homepageTemplate.html', variable=variable)

@app.route('/debug')
def debugPage():
    print('DEBUGGING:')
    lights.alarm_fire()
    return "success"

@app.route('/api/lights/patterns/<pattern>')
def setPattern(pattern):
    print(pattern)
    x = lights.addPattern(pattern)
    print(x)
    return "success"

@app.route('/api/lights/clearPatterns')
def clearPatterns():
    print("suspending patterns")
    lights.suspendAll()
    print("turn off lights")
    patterns.setAll(patterns.RGBColor(0,0,0))
    patterns.strip.show()
    return "success"

@app.route('/api/lights/setStaticColor', methods=['POST'])
def setStaticColor():
    lights.suspendAll()
    red = int(request.form['red'])
    green = int(request.form['green'])
    blue = int(request.form['blue'])
    white = int(request.form['white'])

    print("set static:", (red, green, blue, white))
    patterns.setAll(patterns.RGBColor(red,green,blue,white))
    patterns.strip.show()
    return "success"

@app.route('/api/lights/setAttribute', methods=['POST'])
def setAttribute():
    if request.method == 'POST':
        value = request.form['value']
        attribute = request.form['attribute']
        lights.setAttribute(value, attribute)
        return "success"


@app.route('/api/lights/alarm/<alarmRequest>', methods=["POST"])
def handleAlarmRequest(alarmRequest):
    if alarmRequest == "set":
        unformatted_time = request.form['time']
        formatted = unformatted_time.split(":")
        fire_time = (int(formatted[0]), int(formatted[1]))
        alarm.setAlarm(fire_time, lights.alarm_fire)
        return "success"        
    elif alarmRequest == "status":
        if not alarm.alarm.is_alive():
            alarm.cancelAlarm()
            return "No Alarm Set"
        else: 
            return alarm.alarmTarget
    elif alarmRequest == "cancel":
        alarm.cancelAlarm()
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
            return "success"
        else:
            signature = freqOFF[outletId]
            print(("Turning off " + outletId))
            subprocess.call(('/var/www/rfoutlet/codesend %d -l 180 -p 0' % signature), shell=True)
            return "success"
