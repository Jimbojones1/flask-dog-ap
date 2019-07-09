from flask import Flask, g

import models

from api.api import api


DEBUG = True
PORT = 8000

app = Flask(__name__)

app.register_blueprint(api)

@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)

