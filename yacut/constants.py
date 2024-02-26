"""Константы, используемые в приложении."""

from string import ascii_letters, digits

ALLOWED_CHARS = ascii_letters + digits
REQUEST_BODY_MISSING = "Отсутствует тело запроса"
INVALID_SHORT_URL = "Указано недопустимое имя для короткой ссылки"
FULL_URL_IS_MANDATORY = '"url" является обязательным полем!'
SHORT_URL_EXISTS = "Предложенный вариант короткой ссылки уже существует."
SHORT_URL_NOT_FOUND = "Указанный id не найден"
SHORT_URL_READY = "Ваша новая ссылка готова:"

MAX_LENGTH = 16
MIN_LENGTH = 1
