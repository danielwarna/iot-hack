from flask import Flask, current_app, request
from flask.ext.sqlalchemy import SQLAlchemy

from datetime import datetime

import config

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
        self.sensor = sensor;
        self.value = value


db.create_all()

for i in range(1, 100):
    m = Measurement(datetime.today(), "TEST", 532.22)
    db.session.add(m)

db.session.commit()  


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    return 'Hello World!'


#Hit kommer on event requestar
@app.route('/api', methods=['POST', 'GET'])
def api():
    print "API request"
    print request.get_json()
    return "test"

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
