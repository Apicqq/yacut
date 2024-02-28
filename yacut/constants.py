"""Константы, используемые в приложении."""

from string import ascii_letters, digits

ALLOWED_CHARS_SHORT = ascii_letters + digits
REQUEST_BODY_MISSING = "Отсутствует тело запроса"
INVALID_SHORT = "Указано недопустимое имя для короткой ссылки"
URL_IS_MANDATORY = '"url" является обязательным полем!'
SHORT_EXISTS = "Предложенный вариант короткой ссылки уже существует."
SHORT_NOT_FOUND = "Указанный id не найден"
SHORT_IS_READY = "Ваша новая ссылка готова:"
FORWARDER_FUNC = "forwarder"
FULL_URL = "Длинная ссылка"
MANDATORY_FIELD = "Обязательное поле"
INVALID_URL = "Некорректная ссылка"
USER_SHORT_VARIANT = "Ваш вариант короткой ссылки:"
INVALID_SYMBOLS = "Некорректные символы"
SUBMIT = "Создать"

SHORT_MAX_LENGTH = 16
GENERATED_SHORT_LENGTH = 6
REGEXP_SHORT_VALIDATOR_PATTERN = rf"^[{ALLOWED_CHARS_SHORT}]+$"
MAX_ORIGINAL_LENGTH = 2048
GENERATED_SHORT_RETRIES = 10
