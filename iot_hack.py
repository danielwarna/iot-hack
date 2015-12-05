from flask import Flask, current_app, request, Response, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from graphs import serve_graph, serve_3d_graph
from datetime import datetime

import config
import json

app = Flask(__name__)

app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)


# inout transactions
class Measurement(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime())
    sensor = db.Column(db.String())
    value = db.Column(db.Float())

    def __init__(self, timestamp, sensor, value):
        self.timestamp = timestamp
        self.sensor = sensor
        self.value = value

db.create_all()

def sensor_names(inputstring):
    if inputstring == "0x00050100":
        sens = "longitude"
    elif inputstring == "0x00050200":
        sens = "lateral"
    elif inputstring == "0x00050300":
        sens = "vertical"
    else:
        sens = inputstring
    return sens

def parse(inputString):
    inputstring = inputString.replace("u'", '"')
    inputString = inputstring.replace("'", '"')
    jsonS = json.loads(inputString)
    for i in jsonS:
        for j in i['senses']:
            sens = sensor_names(j['sId'])
            #date = datetime.fromtimestamp(int(str(j['ts'])[:-3]))
            date = datetime.fromtimestamp(j['ts'] / 1000.0)
            m = Measurement(date, sens, j['val'])

            db.session.add(m)

    db.session.commit()


#for i in range(1, 100):
#    m = Measurement(datetime.today(), "TEST", 532.22)
#    db.session.add(m)

#db.session.commit()


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    return 'Hello World!'


#Hit kommer on event requestar
@app.route('/api', methods=['POST', 'GET'])
def api():
    print "API request"
    req = request.get_data()
    print req
    parse(req)
    
    reply = """{
    "timestamp": 1381537803046,
    "added": 1
    }"""

    #1449319059
    #1381537803046

    rep = dict()
    rep['timestamp'] = int(datetime.today().strftime("%s")) * 1000
    rep['added'] = 1   

    reply =json.dumps(rep)

    resp = Response(reply)
    resp.headers["Content-Type"] = "application/json";
    resp.mimetype = "application/json"

    return resp


#Hit kommer generella cloud requests
@app.route('/v2/events', methods=['POST', 'GET'])
def thingsee_in():
    print "Thingsee endpoint"
    print request.get_json()
    return "test"


@app.route('/debug/')
def debug_mode():
    assert current_app.debug == False, "Don't panic! You're here by request of debug()"
    return "aa"


@app.route('/graph/')
def show_graph():
    # TODO get this from database
    sensor_values_1 = [1, 2, 3, 4]
    sensor_values_2 = [4, 3, 2, 1]
    sensor_values_3 = [8, 7, 6, 3]
    # return serve_graph(sensor_values_1, sensor_values_2, sensor_values_3)
    return serve_3d_graph(sensor_values_1, sensor_values_2, sensor_values_3)


@app.route('/graph/js/')
def js_graph():
    lateral = get_sensor_values_from_db("lateral")
    print lateral
    return render_template("jsgraph.html", sensordata=json.dumps(lateral), sensorname="Lateral")


def get_sensor_values_from_db(sensor, fromtime=None, totime=None):

    if fromtime and totime:
        values = Measurement.query.filter(Measurement.sensor == sensor, Measurement.timestamp > fromtime, Measurement.timestamp < totime).order_by(Measurement.timestamp)
    elif fromtime:
        values = Measurement.query.filter(Measurement.sensor == sensor, Measurement.timestamp > fromtime).order_by(Measurement.timestamp)
    elif totime:
        values = Measurement.query.filter(Measurement.sensor == sensor, Measurement.timestamp < totime).order_by(Measurement.timestamp)
    else:
        values = Measurement.query.filter(Measurement.sensor == sensor)
    sensor_data = []
    for v in values:
        sensor_data.append([int(v.timestamp.strftime("%s"))*1000, v.value])

    return sensor_data


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=app.config.get("PORT"))
