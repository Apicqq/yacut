from http import HTTPStatus

from flask import abort, redirect, render_template, flash, url_for

from . import app, forms, constants as const
from .models import URLMap


@app.route("/", methods=("GET", "POST"))
def index_view():
    form = forms.URLForm()
    original, short = form.original_link.data, form.custom_id.data
    if not form.validate_on_submit():
        return render_template("index.html", form=form)
    if URLMap.get(short):
        flash(const.SHORT_EXISTS)
        return render_template("index.html", form=form)
    url_map = URLMap.add(original, short)
    return render_template(
        "index.html",
        form=form,
        result_url=url_for(
            const.FORWARDER_FUNC, short_id=url_map.short, _external=True
        ),
    )


@app.route("/<string:short_id>", methods=("GET",))
def forwarder(short_id):
    original_url = URLMap.get(short_id)
    if original_url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(original_url.original)
