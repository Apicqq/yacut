from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class URLForm(FlaskForm):
    original = URLField(
        "Длинная ссылка",
        validators=[
            DataRequired('Обязательное поле'),
        ]
    )
    custom_url = URLField(
        "Ваш вариант короткой ссылки",
        validators=[Optional(), Length(max=16)]
    )
    submit = SubmitField("Создать")