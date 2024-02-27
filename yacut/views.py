from http import HTTPStatus

from flask import abort, redirect, render_template, flash, url_for
from sqlalchemy.exc import IntegrityError

from . import app, forms, constants as const
from .models import URLMap


@app.route("/", methods=("GET", "POST"))
def index_view():
    form = forms.URLForm()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)
    original = form.original_link.data
    short = form.custom_id.data
    if not short:
        short = URLMap.get_unique_short_id()
    try:
        URLMap.add_url_to_db(original, short)
    except IntegrityError:
        flash(const.SHORT_URI_EXISTS)
    return render_template(
        "index.html",
        form=form,
        result=const.SHORT_URL_READY,
        short=short,
        result_url=url_for(
            const.FORWARDER_FUNC, short_id=short, _external=True
        ),
    )


@app.route("/<string:short_id>", methods=("GET",))
def forwarder(short_id):
    original_url = URLMap.get_original(short_id)
    if original_url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(original_url.original)
