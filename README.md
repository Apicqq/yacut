# О проекте

Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Ключевые возможности сервиса:

- Генерация коротких ссылок и их связь с исходными. Доступен вариант как генерации ссылки, так и использование предложенной пользователем короткой ссылки.
- Переадресация на исходный адрес при обращении к короткой ссылке.

Сервис доступен через WEB и API интерфейсы.

## Использованные технологии:
- Python 3.10
- Flask
- Jinja2
- SQLAlchemy

## Как установить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Apicqq/yacut
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать файл .env:
```
touch .env
```

И наполнить его переменными по примеру файла `.env.example`

Запустить проект:
```
flask run
```

Сервис YaCut будет доступен по адресу: `http://127.0.0.1:5000`

Автор: [Никита Смыков](https://github.com/Apicqq)