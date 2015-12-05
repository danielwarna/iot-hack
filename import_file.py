from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from iot_hack import Measurement, sensor_names
from datetime import datetime
import sys
import config

app = Flask(__name__)

app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)

if len(sys.argv) < 2:
    print "First argument is sdcardtextdump filename"
    exit(1)

filename = sys.argv[1]
f = open(filename, 'r')
for line in f:

        split_data = line.split(';')
        header = split_data[0]
        split_header = header.split(',')
        records = split_data[1:]

        for record in records:
            split_record = record.split(',')

            m = Measurement(
                datetime.fromtimestamp(int(split_record[3]+split_record[4][0:3])/1000.0),
                sensor_names(split_record[1]),
                split_record[2][2:]
            )

            db.session.add(m)

db.session.commit()


