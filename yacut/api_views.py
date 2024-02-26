from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, constants as const
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .processing import (
    check_short_url_exists,
    get_unique_short_id,
    add_url_to_db,
)
from .validators import validate_len, validate_data


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
    short = data.get("custom_id")
    if short:
        validate_len(
            short,
            InvalidAPIUsage(const.INVALID_SHORT_URL, HTTPStatus.BAD_REQUEST),
        )
        validate_data(
            short,
            InvalidAPIUsage(const.INVALID_SHORT_URL, HTTPStatus.BAD_REQUEST),
        )
        if check_short_url_exists(short):
            raise InvalidAPIUsage(
                const.SHORT_URL_EXISTS, HTTPStatus.BAD_REQUEST
            )
    else:
        short = get_unique_short_id()
    add_url_to_db(original, short)
    response = {
        "url": original,
        "short_link": url_for("forwarder", short_id=short, _external=True),
    }
    return jsonify(response), HTTPStatus.CREATED


@app.route("/api/id/<string:short_id>/", methods=("GET",))
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage(const.SHORT_URL_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({"url": url.original}), HTTPStatus.OK
