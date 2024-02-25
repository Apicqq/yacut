from flask import jsonify, request

from . import app, db


@app.route('/api/id/', methods=("POST",))
def add_url():
    pass


@app.route('/api/id/<string:short_id>/', methods=("GET",))
def get_url():
    pass