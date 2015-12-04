from flask import Flask
from flask import current_app, request
from flask import make_response, send_file
import cStringIO

import config

app = Flask(__name__)

app.config.from_object(config.DevelopmentConfig)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/', methods=['POST', 'GET'])
def api():
    print "API request"
    return "test"

@app.route('/v2/events/', methods=['POST', 'GET'])
def thingsee_in():
    print "Thingsee endpoint"
    return "test"
   
"""
@app.route('/debug/')
def debug_mode():
    assert current_app.debug == False, "Don't panic! You're here by request of debug()"
    return "aa"
"""


@app.route('/graph/')
def debug_mode():
    import matplotlib.pyplot as plt
    #plt.plot([1, 2, 3, 4])
    #plt.ylabel('some numbers')
    # plt.show()
    # return "aa"
    #return plt.show()
    #response = make_response(plt.show())
    RAM = cStringIO.StringIO()
    CHART = plt.figure()


    CHART.savefig(RAM, format='png')
    RAM.seek(0)
    return send_file(RAM, mimetype='image/png')

    # response.headers['Content-Type'] = 'image/jpeg'
    # response.headers['Content-Disposition'] = 'attachment; filename=img.jpg'
    # return response


@app.route('/<path:path>', methods=['POST', 'GET'])
def matchall(path):
    print "catch all the things"
    return "test"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
