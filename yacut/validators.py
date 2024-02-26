import re

from typing import NoReturn


def validate_len(
        value: str,
        error: Exception,
        minimum: int = 1,
        maximum: int = 16
) -> NoReturn:
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


def validate_data(value: str, error: Exception) -> NoReturn:
    """
    Проверяет соответствие value регулярному выражению.

    :param value: Передаваемое значение для валидации.
    :param error: Выбрасываемая ошибка.

    :raises InvalidAPIUsage: При недопустимом значении.
    """

    if not re.match(r"^[a-zA-Z0-9]+$", value):
        raise error
