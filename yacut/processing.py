import random

from sqlalchemy.exc import IntegrityError

from .models import URLMap
from .constants import ALLOWED_CHARS
from . import db


def get_unique_short_id(chars=ALLOWED_CHARS, length=6) -> str:
    """
    Генерирует уникальный идентификатор для короткой ссылки.

    :param chars: Символы для генерации уникального идентификатора.
    :param length: Длина уникального идентификатора.

    :returns: Уникальный идентификатор.
    """
    while True:
        short_id = "".join(random.choice(chars) for _ in range(length))
        if URLMap.query.filter_by(short=short_id).first():
            continue
        return short_id


def add_url_to_db(original, short) -> bool:
    """
    Добавляет URLMap в базу данных.

    :param original: Оригинальная ссылка.
    :param short: Короткая ссылка.

    :returns: Факт добавления URLMap в базу данных.
    """
    db.session.add(URLMap(original=original, short=short))
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return True


def check_short_url_exists(short) -> bool:
    """
    Проверяет существование короткой ссылки в базе данных.

    :param short: Короткая ссылка.

    :returns: Факт существования короткой ссылки в базе данных.
    """
    return bool(URLMap.query.filter_by(short=short).first())
