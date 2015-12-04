from flask import Flask
from flask import current_app, request

import config

app = Flask(__name__)

app.config.from_object(config.DevelopmentConfig)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/', methods=['POST', 'GET'])
def thingsee_in():
    print "API request"
    return "test"

@app.route('/debug/')
def debug_mode():
    assert current_app.debug == False, "Don't panic! You're here by request of debug()"
    return "aa"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
