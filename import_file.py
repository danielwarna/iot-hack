from flask import Flask, current_app, request, Response
from flask.ext.sqlalchemy import SQLAlchemy

from iot-hack import Measurement, sensor_names

from datetime import datetime

import config

app = Flask(__name__)

app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)

filename = 'SEND.LOG'
f = open(filename, 'r')
for line in f:

        split_data = line.split(';')
        header = split_data[0]
        split_header = header.split(',')
        records = split_data[1:]

        for record in records:
            split_record = record.split(',')
            m = Measurement(
                datetime.fromtimestamp(header[4]),
                sensor_names(split_record[1]),
                split_record[1][:2]
            )

            db.session.add(m)

db.session.commit()


