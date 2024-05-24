"""
Файл: app/__init__.py
Автор: Андрей Пшеничный
Дата создания: 13 февраля 2024

Этот файл отвечает за инициализацию Flask-приложения, подключение к базе данных и управление маршрутами.

Пример использования:
    Инициализация Flask-приложения и настройка маршрутов:
    ```
    from flask import Flask
    from config import DevelopmentConfig
    from flask_sqlalchemy import SQLAlchemy
    
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db = SQLAlchemy(app)
    
    from app import routes, models, history_handlers
    ```
Описание модуля history_handlers:
    Модуль history_handlers содержит слушателя событий для модели ModelAccum, который автоматически создает записи в таблице History при обновлении объектов.
    
Примеры:
    - Инициализация объекта Flask-приложения.
    - Подключение к базе данных с помощью SQLAlchemy.
    - Импорт и использование маршрутов(routes) и моделей(models) для Flask-приложения.
    - Автоматическое создание и добавление записи в таблицу History при обновлении объектов модели ModelAccum с помощью слушателя событий.
"""
from flask import Flask
from config import ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from . import decorators

app = Flask(__name__)
app.config.from_object(ProductionConfig)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)  # Инициализация расширения Flask-Mail


from app import models
from app.routes import view_pages
from app.routes import view_tables
from app.routes import user_functions
from app.routes import data_request_server 
from app.routes import data_entry_functions
from app.routes import data_deletion_functions
from app.routes import data_modification_functions

from app.listener_functions import listenCity
from app.listener_functions import listenUser




