#!/usr/bin/env python
import json
import random
import time
import ast
import codecs
import subprocess
import jsonlines

from datetime import datetime

from flask import Flask, Response, render_template, jsonify

app = Flask(__name__)
random.seed()  # Initialize the random number generator

#===== configs =======
#file locations and lines to be read form tail: 
accellogPath = "./PDD/logs/accellog.json"
accellogLineNum = 30  # sensor => 20 record/sec, some delay
accelSleepTime = 0.1


hblogPath = "./PDD/logs/hblog.json"
hblogPathLineNum = 10
hbSleepTime = 0.5

spo2logPath = "./PDD/logs/spo2log.json"
spo2logLineNum = 10
spo2SleepTime = 0.5

srlogPath = "./PDD/logs/skinreslog.json"
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

def getJsonDataLoop(path, tailLines, sleepTime, processFunc):
    while True:
        # this is raw data, need to convert to time value
        #eg. {'time': datetime.now().strftime('%H:%M:%S'), 'value': data['hr']}
        dataArray = getLastLinesFromFile(tailLines, path)
        data = processFunc(dataArray)
        yield processFunc(dataArray)
        # print ("data:{}\n\n".format(responseData))
        time.sleep(sleepTime)


#=======algorithm==========
def getAccel(array):
    lastMag = 0
    motion='stationary'
    for record in array:
        mag = record['magnitude']
        diff = abs(mag - lastMag)
        if (abs(mag) > 0.2 ):
            motion = 'stationary'
        if (abs(mag) > 2):
            motion = 'constant motion'
        if (mag > 7):
            motion = 'jerked'
        lastMag = mag

    json_data = json.dumps({'value': motion})

    return "data:{}\n\n".format(json_data)
    


def getAvgHB(array):
    total = 0
    for record in array:
        total = total + record['BPM']
    avg = int(total/len(array))
    json_data = json.dumps({'time': datetime.now().strftime('%H:%M:%S'), 'value': avg})
    return "data:{}\n\n".format(json_data)

def getAvSpo2(array):
    total = 0
    for record in array:
        total = total + record['SPO2']
    avg = int(total/len(array))
    json_data = json.dumps({'time': datetime.now().strftime('%H:%M:%S'), 'value': avg})
    return "data:{}\n\n".format(json_data)

def getAvSr(array):
    total = 0
    for record in array:
        total = total + record['Resistance']
        
    avg = int(total/len(array))
    json_data = json.dumps({'time': datetime.now().strftime('%H:%M:%S'), 'value': avg})
    return "data:{}\n\n".format(json_data)


def getAvTemp(array):
    total = 0
    for record in array:
        total = total + record['Temp']
    avg = int(total/len(array))
    json_data = json.dumps({'time': datetime.now().strftime('%H:%M:%S'), 'value': avg})
    return "data:{}\n\n".format(json_data)
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
       return getJsonDataLoop(accellogPath, accellogLineNum, accelSleepTime, getAccel)
    return Response(getData(), mimetype='text/event-stream')

@app.route('/chart-data/hb')
def chart_data2():
    def getData():
        return getJsonDataLoop(hblogPath, hblogPathLineNum, hbSleepTime, getAvgHB)
    return Response(getData(), mimetype='text/event-stream')

@app.route('/chart-data/spo2')
def chart_data3():
    def getData():
        return getJsonDataLoop(spo2logPath, spo2logLineNum, spo2SleepTime, getAvSpo2)
    return Response(getData(), mimetype='text/event-stream')

@app.route('/chart-data/sr')
def chart_data4():
    def getData():
        return getJsonDataLoop(srlogPath, srlogPathLineNum, srlogPathSleepTime,getAvSr)
    return Response(getData(), mimetype='text/event-stream')

@app.route('/chart-data/temp')
def chart_data5():
    def getData():
        return getJsonDataLoop(templogPath, templogPathLineNum, templogPathSleepTime,getAvTemp)
    return Response(getData(), mimetype='text/event-stream')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True, threaded=True)
