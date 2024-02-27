from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from . import constants as const


class URLForm(FlaskForm):
    original_link = URLField(
        const.FULL_URL,
        validators=[
            DataRequired(const.URL_IS_MANDATORY),
            URL(message=const.INVALID_URL),
            Length(
                max=const.MAX_ORIGINAL_URL_LENGTH,
                message=const.INVALID_SYMBOLS,
            ),
        ],
    )
    custom_id = URLField(
        const.USER_SHORT_VARIANT,
        validators=[
            Optional(),
            Length(max=const.SHORT_MAX_LENGTH),
            Regexp(
                const.REGEXP_SHORT_VALIDATOR_PATTERN,
                message=const.INVALID_SYMBOLS,
            ),
        ],
    )
    submit = SubmitField(const.SUBMIT)
