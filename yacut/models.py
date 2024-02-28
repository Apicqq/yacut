import random
import re
from datetime import datetime as dt

from . import constants as const, db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text(const.MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(
        db.String(const.SHORT_MAX_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, nullable=False, default=dt.now)

    @staticmethod
    def get(short):
        """
        Возвращает оригинальную ссылку по короткой ссылке.

        :param short: Короткая ссылка.
        """
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def add(original: str, short: str) -> "URLMap":
        """
        Добавляет URLMap в базу данных.

        :param original: Оригинальная ссылка.
        :param short: Короткая ссылка.

        :returns: Добавленный URLMap.
        """
        if original and (
            not re.match(const.REGEXP_FULL_VALIDATOR_PATTERN, original)
            or len(original) > const.MAX_ORIGINAL_LENGTH
        ):
            raise TypeError(const.INVALID_URL)
        #  Не придумал, какое тут бросить исключение,
        #  ведь я не могу включать в этот код свои собственные
        if short:
            if URLMap.get(short):
                raise RuntimeError(const.SHORT_EXISTS)
            if len(short) > const.SHORT_MAX_LENGTH or not re.match(
                const.REGEXP_SHORT_VALIDATOR_PATTERN, short
            ):
                raise ValueError(const.INVALID_SHORT)
        else:
            short = URLMap.get_unique_short_id()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_unique_short_id(
        chars=const.ALLOWED_CHARS_SHORT, length=const.GENERATED_SHORT_LENGTH
    ) -> str:
        """
        Генерирует уникальный идентификатор для короткой ссылки.

        :param chars: Символы для генерации уникального идентификатора.
        :param length: Длина уникального идентификатора.

        :returns: Уникальный идентификатор.
        """
        for _ in range(const.GENERATED_SHORT_RETRIES):
            short_id = "".join(random.sample(chars, length))
            if URLMap.get(short_id):
                continue
            return short_id
