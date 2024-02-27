import random
import re
from datetime import datetime as dt
from http import HTTPStatus

from . import constants as const
from . import db
from .error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(const.MAX_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=dt.now)

    @classmethod
    def create_short(cls, short):
        if short:
            cls.validate_len(
                short,
                InvalidAPIUsage(const.INVALID_SHORT_URL,
                                HTTPStatus.BAD_REQUEST),
            )
            cls.validate_data(
                short,
                InvalidAPIUsage(const.INVALID_SHORT_URL,
                                HTTPStatus.BAD_REQUEST),
            )
            if bool(cls.get_original(short)):
                raise InvalidAPIUsage(
                    const.SHORT_URI_EXISTS, HTTPStatus.BAD_REQUEST
                )
        else:
            short = cls.get_unique_short_id()
        return short

    @classmethod
    def get_by_short(cls, short):
        """
        Возвращает оригинальную ссылку по короткой ссылке.
        Используется для API-запросов.

        :param short: Короткая ссылка.

        :raises InvalidAPIUsage: Если не найдена оригинальная
         ссылка по короткой ссылке.
        """
        url = cls.get_original(short)
        if not url:
            raise InvalidAPIUsage(const.SHORT_URI_NOT_FOUND,
                                  HTTPStatus.NOT_FOUND)
        return url

    @classmethod
    def get_original(cls, short):
        """
        Возвращает оригинальную ссылку по короткой ссылке.

        :param short: Короткая ссылка.
        """
        return cls.query.filter_by(short=short).first()

    @classmethod
    def add_url_to_db(cls, original, short):
        """
        Добавляет URLMap в базу данных.

        :param original: Оригинальная ссылка.
        :param short: Короткая ссылка.

        :returns: Добавленный URLMap.
        """
        db.session.add(URLMap(original=original, short=short))
        db.session.commit()
        return URLMap(original=original, short=short)

    @classmethod
    def get_unique_short_id(
            cls,
            chars=const.ALLOWED_CHARS,
            length=const.SHORT_URL_LENGTH
    ) -> str:
        """
        Генерирует уникальный идентификатор для короткой ссылки.

        :param chars: Символы для генерации уникального идентификатора.
        :param length: Длина уникального идентификатора.

        :returns: Уникальный идентификатор.
        """
        short_id = "".join(random.sample(chars, length))
        return short_id if not bool(
            cls.get_original(short_id)
        ) else cls.get_unique_short_id()

    @classmethod
    def validate_len(
            cls,
            value: str,
            error: Exception,
            minimum: int = const.MIN_LENGTH,
            maximum: int = const.MAX_LENGTH
    ) -> None:
        """
        Проверяет длину value на соответствие заданному диапазону.

        :param value: Передаваемое значение для валидации.
        :param error: Выбрасываемая ошибка.
        :param minimum: Минимально допустимая длина.
        :param maximum: Максимально допустимая длина.

        :raises InvalidAPIUsage: При недопустимой длине.
        """
        if len(value) < minimum or len(value) > maximum:
            raise error

    @classmethod
    def validate_data(cls, value: str, error: Exception) -> None:
        """
        Проверяет соответствие value регулярному выражению.

        :param value: Передаваемое значение для валидации.
        :param error: Выбрасываемая ошибка.

        :raises InvalidAPIUsage: При недопустимом значении.
        """

        if not re.match(fr"^[{const.ALLOWED_CHARS}]+$", value):
            raise error



