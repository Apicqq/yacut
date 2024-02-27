"""Константы, используемые в приложении."""

from string import ascii_letters, digits

ALLOWED_CHARS = ascii_letters + digits
REQUEST_BODY_MISSING = "Отсутствует тело запроса"
INVALID_SHORT_URL = "Указано недопустимое имя для короткой ссылки"
FULL_URL_IS_MANDATORY = '"url" является обязательным полем!'
SHORT_URI_EXISTS = "Предложенный вариант короткой ссылки уже существует."
SHORT_URI_NOT_FOUND = "Указанный id не найден"
SHORT_URL_READY = "Ваша новая ссылка готова:"
FORWARDER_FUNC = "forwarder"
FULL_URL = "Длинная ссылка"
MANDATORY_FIELD = "Обязательное поле"
INVALID_URL = "Некорректная ссылка"
USER_SHORT_URL_VARIANT = "Ваш вариант короткой ссылки:"
INVALID_SYMBOLS = "Некорректные символы"
SUBMIT = "Создать"

MIN_LENGTH = 1
MAX_LENGTH = 16
SHORT_URL_LENGTH = 6
