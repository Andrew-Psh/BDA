"""
Файл: text_select_field.py

Описание:
Этот файл содержит реализацию веб-приложения с использованием Flask для обработки запросов и отображения веб-страниц.

Пример использования:
1. Установите переменную окружения "FLASK_APP", используя следующие команды в зависимости от вашей операционной системы:
   - Unix/Linux:
     export FLASK_APP=search_field_application.py
   - Windows:
     set FLASK_APP=search_field_application.py

2. После настройки переменной окружения "FLASK_APP" запустите приложение Flask с помощью команды:
   flask run
   или
   python -m flask run

Автоматическая перезагрузка для приложений Flask во время реального разработки может быть включена с помощью функции "автоперезагрузка" по следующим шагам:
1. Установите пакет Werkzeug, который предоставляет инструменты для автоматической перезагрузки:
   pip install Werkzeug

2. Установите переменную окружения FLASK_ENV в "development", чтобы включить режим разработки Flask:
   - Unix/Linux/MacOS:
     export FLASK_ENV=development
   - Windows:
     set FLASK_ENV=development

3. Запустите ваше приложение Flask следующей командой:
   flask run
   ИЛИ в режиме DEBUG:
   flask run --debug

Чтобы запустить оболочку в контексте приложения Flask, используйте команду "flask shell".
Эта команда открывает интерактивную оболочку, где можно взаимодействовать с приложением Flask и его моделями.
Вот как это сделать:

1. Откройте терминал или командную строку.

2. Перейдите в каталог, где находится ваше приложение Flask (включая файл "text_select_field.py").

3. Выполните следующую команду для запуска оболочки Flask:
   flask shell

4. После запуска оболочки Flask вы сможете взаимодействовать с вашими моделями, выполнять запросы к базе данных и другие задачи
   в контексте вашего приложения Flask.   

Реализация:
- Сценарий инициализирует приложение Flask и соединения с базой данных.
- Загружает переменные окружения из файла .env для конфигурации.
- Задает контекст оболочки для взаимодействия с моделями в сеансах оболочки Flask.
"""

from app import app, db
from app.models import  Accum, Node, Equipment, State, History, ModelAccum, City

@app.shell_context_processor
def make_shell_context():
   '''
   Запустите оболочку в контексте приложения, используя команду "flask shell".    
   '''
   return {'db': db, 
           'Accum': Accum, 
           'Node': Node,
           'Equipment': Equipment,
           'State': State,
           'History': History,
           'ModelAccum': ModelAccum,
           'City': City
           }