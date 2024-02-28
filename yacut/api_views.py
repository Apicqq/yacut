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
    original, short = data.get("url"), data.get("custom_id")
    if original is None:
        raise InvalidAPIUsage(const.URL_IS_MANDATORY, HTTPStatus.BAD_REQUEST)
    try:
        url_map = URLMap.add(original, short)
    except RuntimeError:
        raise InvalidAPIUsage(const.SHORT_EXISTS, HTTPStatus.BAD_REQUEST)
    except ValueError:
        raise InvalidAPIUsage(const.INVALID_SHORT, HTTPStatus.BAD_REQUEST)
    except TypeError:
        raise InvalidAPIUsage(const.INVALID_URL, HTTPStatus.BAD_REQUEST)
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
    original = URLMap.get(short)
    if not original:
        raise InvalidAPIUsage(const.SHORT_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return (
        jsonify({"url": original.original}),
        HTTPStatus.OK,
    )
