from flask import Flask
from flask import current_app, request

import config

app = Flask(__name__)

app.config.from_object(config.DevelopmentConfig)

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
