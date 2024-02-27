from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from . import constants as const


class URLForm(FlaskForm):
    original_link = URLField(
        const.FULL_URL,
        validators=[
            DataRequired(const.FULL_URL_IS_MANDATORY),
            URL(message=const.INVALID_URL),
            Length(min=const.MIN_LENGTH, message=const.INVALID_SYMBOLS),
        ],
    )
    custom_id = URLField(
        const.USER_SHORT_URL_VARIANT,
        validators=[
            Optional(),
            Length(max=const.MAX_LENGTH),
            Regexp(rf"[{const.ALLOWED_CHARS}]", message=const.INVALID_SYMBOLS),
        ],
    )
    submit = SubmitField(const.SUBMIT)
