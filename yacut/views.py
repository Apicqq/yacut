from http import HTTPStatus

from flask import abort, redirect, render_template, flash, url_for

from . import app, forms, constants as const
from .error_handlers import ShortExistsException
from .models import URLMap


@app.route("/", methods=("GET", "POST"))
def index_view():
    form = forms.URLForm()
    if not form.validate_on_submit():
        return render_template("index.html", form=form)
    try:
        url_map = URLMap.add(
            form.original_link.data, form.custom_id.data, validate=False
        )
    except (ShortExistsException, RuntimeError) as exception:
        flash(str(exception))
        return render_template("index.html", form=form)
    return render_template(
        "index.html",
        form=form,
        result_url=url_for(
            const.FORWARDER_FUNC, short=url_map.short, _external=True
        ),
    )


@app.route("/<string:short>", methods=("GET",))
def forwarder(short):
    url_map = URLMap.get(short)
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
