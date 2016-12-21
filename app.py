#!/usr/bin/env python

import urllib
import json
import os


from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "findSchedule":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    direction = parameters.get("direction")
    reqTime=parameters.get("time")
    station= parameters.get("stations")
    period=parameters.get("period")
    #count=parameters.get("number")
    #print(station)
    hours,mins,secs=map(int,reqTime.split(':'))
    schedule=""
    if station.lower() == "dunwoody":
        if direction.lower() == "south":
            schedule={'11':'11:02AM,11:15AM,11:25AM,11:40AM,11:55AM'}
            print(str(schedule[hours]))
        else:
            schedule={'23':'11:02PM,11:15PM,11:25PM'}
    else:
        print "not dunwoody"
   
    speech = "The next trains from  " + station + " are at " + str(schedule[hours]) + " respectively."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "mymarta-data"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
