import random
import re
from datetime import datetime as dt

from . import constants as const, db
from .error_handlers import (
    InvalidURLException,
    InvalidShortException,
    ShortExistsException,
)


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
    def add(original: str, short: str, validate: bool = True) -> "URLMap":
        """
        Добавляет URLMap в базу данных. Валидирует входящие параметры,
        если они существуют. В случае провала валидации
        выбрасывает соответствующее исключение.

        :param original: Оригинальная ссылка.
        :param short: Короткая ссылка.
        :param validate: Флаг, пропускающий некоторые проверки в случае,
         если необходимо проверить только наличие короткого идентификатора
         в БД.

        :returns: Добавленный URLMap.

        :raises InvalidShortException: Если короткая ссылка
         не прошла валидацию.
        :raises InvalidURLException: Если оригинальная ссылка
         не прошла валидацию.
        :raises ShortExistsException: Если короткая ссылка уже существует.
        """
        if validate:
            if len(original) > const.MAX_ORIGINAL_LENGTH:
                raise InvalidURLException(const.INVALID_URL)
            if short:
                if len(short) > const.SHORT_MAX_LENGTH or not re.match(
                    const.REGEXP_SHORT_VALIDATOR_PATTERN, short
                ):
                    raise InvalidShortException(const.INVALID_SHORT)
        if short:
            if URLMap.get(short):
                raise ShortExistsException(const.SHORT_EXISTS)
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

        :raises RuntimeError: В случае, если не удалось сгенерировать
         уникальный идентификатор.
        """
        for _ in range(const.GENERATED_SHORT_RETRIES):
            short_id = "".join(random.sample(chars, length))
            if not URLMap.get(short_id):
                return short_id
        raise RuntimeError(const.ERROR_WHILE_GENERATING_SHORT)
