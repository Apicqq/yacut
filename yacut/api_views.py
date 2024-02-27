from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, constants as const
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route("/api/id/", methods=("POST",))
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(
            const.REQUEST_BODY_MISSING, HTTPStatus.BAD_REQUEST
        )
    original = data.get("url")
    if original is None:
        raise InvalidAPIUsage(
            const.FULL_URL_IS_MANDATORY, HTTPStatus.BAD_REQUEST
        )
    prepared_url = URLMap.add_url_to_db(
        original, URLMap.create_short(data.get("custom_id"))
    )
    response = {
        "url": prepared_url.original,
        "short_link": url_for(
            const.FORWARDER_FUNC, short_id=prepared_url.short, _external=True
        ),
    }
    return jsonify(response), HTTPStatus.CREATED


@app.route("/api/id/<string:short_id>/", methods=("GET",))
def get_url(short_id):
    return (
        jsonify({"url": URLMap.get_by_short(short_id).original}),
        HTTPStatus.OK,
    )
