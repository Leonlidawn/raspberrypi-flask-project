#!/usr/bin/env python
import json
import random
import time
import ast
import codecs
import subprocess
import jsonlines

from datetime import datetime

from flask import Flask, Response, render_template

app = Flask(__name__)
random.seed()  # Initialize the random number generator

#===== configs =======
#file locations and lines to be read form tail:
accellogPath = "./PDD/logs/accellog.json"
accellogLineNum = 10
accelSleepTime = 0.5

hblogPath = "./PDD/logs/hblog.json"
hblogPathLineNum = 10
hbSleepTime = 0.25

spo2logPath = "./PDD/logs/spo2log.json"
spo2logLineNum = 10
spo2SleepTime = 0.5

srlogPath = "./PDD/logs/srlog.json"
srlogPathLineNum = 10
srlogPathSleepTime = 1

templogPath = "./PDD/logs/templog.json"
templogPathLineNum = 10
templogPathSleepTime = 1
#===== log variables for calculation, apply algo here ==========

#accel
#response: {magnitute, delta slop, status<trembling | idle | jerk> }

#hr
#response: {hr, , status<>}
#

#==shared functions==========

def getLastLinesFromFile(numLines, filename):
    command = "tail -n "+str(numLines)+" "+filename
    result = runShellCommand(command).decode()
    jsonArray = []
    array = result.split("\n")
    for i in array:
        #json.loads doesnt work?
        if i.strip() != "" :
            record = json.loads(i)
            jsonArray.append(record)
    return jsonArray

def runShellCommand(command):
    out = subprocess.run(
        command.split(" "),
        stdout=subprocess.PIPE) 
    return out.stdout


def getJsonDataLoop(path, tailLines, sleepTime):
        while True:
            json_data = json.dumps({'time': datetime.now().strftime('%H:%M:%S'), 'value': 1})
            # this is raw data, need to convert to time value
            #eg. {'time': datetime.now().strftime('%H:%M:%S'), 'value': data['hr']}
            responseData = getLastLinesFromFile(tailLines, path)
            # print ("data:{}\n\n".format(responseData))
            time.sleep(sleepTime)

#=======algorithm==========



#======routes===========
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/patient')
def patient():
    name = str(random.randint(0,100000))
    data=json.dumps({"name":name}),
    return Response(data,mimetype='application/json')

@app.route('/chart-data/accel')
def chart_data1():
    def getData():
        getJsonDataLoop(accellogPath, accellogLineNum, accelSleepTime)
    return Response(getData(), mimetype='text/event-stream')

@app.route('/chart-data/hb')
def chart_data2():
    def getData():
        getJsonDataLoop(hblogPath, hblogPathLineNum, hbSleepTime)
    return Response(getData(), mimetype='text/event-stream')

@app.route('/chart-data/spo2')
def chart_data3():
    def getData():
        getJsonDataLoop(spo2logPath, spo2logLineNum, spo2SleepTime)
    return Response(getData(), mimetype='text/event-stream')

@app.route('/chart-data/sr')
def chart_data4():
    def getData():
        getJsonDataLoop(spo2logPath, srlogPathLineNum, srlogPathSleepTime)
    return Response(getData(), mimetype='text/event-stream')

@app.route('/chart-data/temp')
def chart_data5():
    def getData():
        getJsonDataLoop(templogPath, templogPathLineNum, templogPathSleepTime)
    return Response(getData(), mimetype='text/event-stream')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True, threaded=True)
