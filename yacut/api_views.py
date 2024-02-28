from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, constants as const
from .error_handlers import (
    InvalidAPIUsage,
)
from .models import URLMap


@app.route("/api/id/", methods=("POST",))
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(
            const.REQUEST_BODY_MISSING, HTTPStatus.BAD_REQUEST
        )
    if data.get("url") is None:
        raise InvalidAPIUsage(const.URL_IS_MANDATORY, HTTPStatus.BAD_REQUEST)
    try:
        url_map = URLMap.add(data.get("url"), data.get("custom_id"))
    except Exception as exception:
        raise InvalidAPIUsage(exception.args[0])
    return (
        jsonify(
            {
                "url": url_map.original,
                "short_link": url_for(
                    const.FORWARDER_FUNC,
                    short=url_map.short,
                    _external=True,
                ),
            }
        ),
        HTTPStatus.CREATED,
    )


@app.route("/api/id/<string:short>/", methods=("GET",))
def get_url(short):
    url_map = URLMap.get(short)
    if not url_map:
        raise InvalidAPIUsage(const.SHORT_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return (
        jsonify({"url": url_map.original}),
        HTTPStatus.OK,
    )
