# Название вашего проекта

## Описание
Краткое описание вашего проекта и его цели.


## Установка
1. Клонировать репозиторий: git clone https://github.com/Andrew-Psh/BDA
2. Убедитесь, что у вас установлена версия Python указанная в файле runtime.txt (например, python-3.12.1).
3. Установить виртуальное окружение (рекомендуется): 
    - Создайте виртуальное окружение:   `python3 -m venv venv`
    - Активируйте виртуальное окружение:
        - Для Windows:                  `venv\Scripts\activate`
        - Для MacOS/Linux:              `source venv/bin/activate`
4. Обновить pip:                        `pip install --upgrade pip`   
5. Установить python-dotenv:            `pip install python-dotenv==1.0.1` 
6. Внести необходимые изменения  в файл .env 
    - задать свой SECRET_KEY = 'you_secret_key' 
    - задать точку входа в приложение 
        FLASK_APP=search_field_application.py
    - Доступ к демонстрационной БД 
        SQLITE_FILE_NAME = 'sqlite_file_name.db'
    - При необходимости тут можно поключить свою  БД
         DATABASE_URL = 'mysql+pymysql://root:sqaz21typ@localhost/db_name'
7. Установить зависимости:              pip install -r requirements.txt


### Шаги для настройки MySQL в файле .env:
1. Создайте или откройте файл .env в корневой папке проекта.
2. Добавьте следующие строки в файл .env, указав конкретные значения для переменных:
    ```
    SECRET_KEY=your_secret_key
    DATABASE_URL=mysql+pymysql://root:sqaz21typ@localhost/db_name
    ```

### Шаги для выбора конфигурации в файле __init__.py:
3. Обновите блок кода в файле `config.py` с необходимыми конфигурациями

4. В файле __init__.py выберите соответствующую конфигурацию
## Структура проекта

```bash
tree -I 'venv'

search_field_application/
├── app
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
|   ├── history_handlers.py
│   ├── static
│   │   ├── css
│   │   │   ├── body_styles.css
│   │   │   ├── flashed_messages.css
│   │   │   ├── form_styles.css
│   │   │   ├── navigation_styles.css
│   │   │   ├── reset.css
│   │   │   └── styles.css
│   │   ├── fonts
│   │   ├── images
│   │   └── js
│   │       ├── dsf.js
│   │       └── dsf_bacup.js
│   └── templates
│       ├── add_user.html
│       ├── common
│       │   ├── base.html
│       │   ├── flashed_messages.html
│       │   ├── index.html
│       │   ├── nav_base.html
│       │   └── nav_base_bacup.html
│       ├── samples
│       │   ├── dinamic_select_field.html
│       │   └── field.html
│       └── utilites
│           └── json_file_form.html
├── config.py
├── db_loader_and_json
│   ├── __pycache__
│   │   └── db_loader.cpython-312.pyc
│   ├── colors.json
│   ├── db_loader.py
│   └── users.json
├── doc.md
├── readme.md
├── requirements.txt
├── runtime.txt
└── search_field_application.py

13 directories, 31 files
```

## Консольные команды
- Запуск приложения в режиме отладки: flask run
- Запуск приложения в режиме отладки с автоматическим перезапуском: flask run --reload
- Запуск оболочки Flask: flask shell


## Работа с базой данных SQLAlchemy

### Основные команды SQLAlchemy:

- Создание таблиц в базе данных (если не созданы): `db.create_all()`
- Сохранение изменений в базе данных: `db.session.commit()`
- Откат последнего миграционного изменения: `flask db downgrade`
- Применение миграций к базе данных: `flask db upgrade`

### Операции с базой данных:

#### Добавление записи:
```python
new_entry = YourModelName(column1='value1', column2='value2')
db.session.add(new_entry)
db.session.commit()
```

#### Удаление записи:
```python
entry_to_delete = YourModelName.query.filter_by(id=1).first()
db.session.delete(entry_to_delete)
db.session.commit()
```

#### Выборка записей:
```python
data = db.session.query(YourModelName).filter(YourModelName.column == 'value').all()
```


## Примеры использования
Примеры того, как использовать ваше приложение или его функциональность.

## Лицензия
Укажите информацию о лицензии вашего проекта.

## Контакты
Дополнительная информация для связи или обратной связи.


# валидаци email в  WTForm
 pip install "wtforms[email]"