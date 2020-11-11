#!/usr/bin/env python
import json
import random
import time
import ast
import codecs


from datetime import datetime

from flask import Flask, Response, render_template

app = Flask(__name__)
random.seed()  # Initialize the random number generator

def getData():
        try:
            file = open("data.txt","r")
            contents = file.read()
            data = ast.literal_eval(contents)
            file.close()
            return data
        except Exception, ex:
            return str(ex)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chart-data')
def chart_data():
    def getJsonData():
        while True:
            data = getData()
            print ("data:{}\n\n".format(data))
            json_data = json.dumps(
                # change this to read from file
                {'time': datetime.now().strftime('%H:%M:%S'), 'value': data['hr']})
            yield ("data:{}\n\n".format(json_data))
            time.sleep(1)

    return Response(getJsonData(), mimetype='text/event-stream')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
