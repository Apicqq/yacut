from http import HTTPStatus

from flask import abort, redirect, render_template

from . import app
from . import forms, models


@app.route('/', methods=("GET", "POST"))
def index_view():
    form = forms.URLForm()
    if form.validate_on_submit():
        ...
    return render_template('index.html', form=form)


@app.route('/<string:short_id>/', methods=("GET",))
def redirecter(short_id):
    original_url = models.URLMap.query.filter_by(short=short_id).first()
    if original_url is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(original_url.original)
