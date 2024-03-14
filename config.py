"""
Файл: config.py
Автор: Андрей Пшеничный
Дата создания: 13 февраля 2024

Описание:
Этот файл содержит настройки конфигурации для Flask-SQLAlchemy. Классы конфигурации определяют различные наборы настроек
для сред разработки и производства, используя переменные среды.

Использование:
- Импортируйте необходимые модули.
- Установите секретный ключ приложения Flask, предоставив его через переменную среды 'SECRET_KEY'.
- Создайте экземпляр класса Config для общих настроек.
- Используйте класс DevelopmentConfig при запуске приложения в среде разработки. Он определяет путь к базе данных SQLite
  на основе переменной среды 'SQLITE_FILE_NAME'.
- Класс ProductionConfig используется для среды производства, где URI базы данных устанавливается с использованием
  переменной среды 'DATABASE_URL'.

Примечание:
Для получения более подробной информации о создании конфигурационного файла Flask-SQLAlchemy обратитесь к официальной документации
по ссылке:
http://flask-sqlalchemy.pocoo.org/2.1/config/
"""

from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, os.environ.get('SQLITE_FILE_NAME'))

class ProductionConfig(Config):
    # DATABASE_URL='mysql+mysqlconnector://black_cat:sqwerty21p@localhost/dba'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
