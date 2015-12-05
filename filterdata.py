from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from iot_hack import Measurement, sensor_names, DataOfIntrest
from datetime import datetime
import sys
import config
import numpy

app = Flask(__name__)

app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)

treshhold = 0.3

def computeStdDev(data):
    dat = dict()

    dat['longitude'] = list()
    dat['lateral'] = list()
    dat['vertical'] = list()

    for d in data:
        dat[d.sensor].append(d.value)
    
    dat['longitude'] = numpy.std(dat['longitude'])
    dat['lateral'] = numpy.std(dat['lateral'])
    dat['vertical'] = numpy.std(dat['vertical'])

    return numpy.average([dat['longitude'], dat['lateral'], dat['vertical']])

    return dat


def runFilter():
    running = True
    limitRange = 150
    limitIncrement = 100

    starttimestamp = 0

    #Setting first values

    startobj = Measurement.query.order_by(Measurement.timestamp).first()
    print startobj.timestamp

    startlimit = 0

    while running:
        endlimit = startlimit + limitRange
        measures = Measurement.query.order_by(Measurement.timestamp).slice(startlimit, endlimit)
        
        stdev = computeStdDev(measures)

        if measures.count() != limitRange:
            running = False

        print "Start: ", startlimit, "  stdev: ", stdev

        if stdev > treshhold:
            doi = DataOfIntrest(measures[0].timestamp, measures[-1].timestamp, stdev)
            db.session.add(doi)
            db.session.commit()
            #print "Committing"

        startlimit += limitIncrement


runFilter()