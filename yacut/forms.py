from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp


class URLForm(FlaskForm):
    original_link = URLField(
        "Длинная ссылка",
        validators=[
            DataRequired('Обязательное поле'),
            URL(message='Некорректная ссылка'),
        ]
    )
    custom_id = URLField(
        "Ваш вариант короткой ссылки. До 16 символов",
        validators=[Optional(), Length(max=16),
                    Regexp(r"\w{0,16}", message="Недопустимые символы")],
    )
    submit = SubmitField("Создать")
