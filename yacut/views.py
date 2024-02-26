from http import HTTPStatus

from flask import abort, redirect, render_template, flash

from . import app, forms, models, constants as const
from .processing import get_unique_short_id, add_url_to_db


@app.route("/", methods=("GET", "POST"))
def index_view():
    form = forms.URLForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        if not add_url_to_db(original, short):
            flash(const.SHORT_URL_EXISTS)
            return render_template("index.html", form=form)
        flash(const.SHORT_URL_READY)
        flash(short)
    return render_template("index.html", form=form)


@app.route("/<string:short_id>", methods=("GET",))
def forwarder(short_id):
    original_url = models.URLMap.query.filter_by(short=short_id).first()
    if original_url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(original_url.original)
