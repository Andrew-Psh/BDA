"""
Файл: db_loader_and_json/db_loader.py
Автор: Андрей Пшеничный
Дата создания: 13 февраля 2024

Описание:
Модуль `db_loader.py` предоставляет функцию `load_data_from_json()`, которая загружает данные из JSON файла в базу данных.

Основные функции:
- load_data_from_json(json_file, model_name): Загружает данные из JSON файла в модель базы данных.

Примеры использования:
1. Загрузка данных пользователя из файла 'users.json':
   load_data_from_json('users.json', 'User')
2. Загрузка данных цветов из файла 'colors.json':
   load_data_from_json('colors.json', 'Color')
"""

from flask import flash
import json
from datetime import datetime
from app.models import Accum, City, Node, Equipment, State, ModelAccum, History
from app import db  
import os
from sqlalchemy.inspection import inspect

def load_data_from_json(json_file, model_name):
    """
    Загружает данные из JSON файла в базу данных.

    Для успешной загрузки данных, структура данных в JSON файле 
    должна соответствовать структуре модели с указанным именем.

    Аргументы:
    json_file (str): Имя JSON файла для загрузки данных.
    model_name (str): Имя модели для загрузки данных из JSON.

    Возвращает:
    str: Сообщение о завершении загрузки данных.

    Пример использования:
    load_data_from_json('users.json', 'User')
    """
    # Открываем и считываем JSON файл
    with open(os.path.join('utilities/json_files', json_file)) as file:
        data = json.load(file)
        # model_choices = {'Color': Color, 'Character': Character}  # Словарь для выбора модели по имени

        model_choices = {'Accum': Accum, 'City': City, 'Node': Node, 'Equipment': Equipment, 'State': State, 'ModelAccum': ModelAccum, 'History': History}  # Словарь для выбора модели по имени
        model = model_choices.get(model_name)  # Получение соответствующей модели

        if model:
            # Получение списка имен столбцов из модели
            column_names = [column.key for column in inspect(model).c if column.key != 'id']             

            # Проверяем соответствие столбцов модели данным из JSON
            for item_data in data:
                if set(item_data.keys()) == set(column_names):
                    # Создаем объект модели и проверяем его наличие в базе
                    if 'd_prod' in item_data:
                        item_data['d_prod'] = datetime.strptime(item_data['d_prod'], '%Y-%m-%d')
                    if 'd_edit' in item_data:
                        item_data['d_edit'] = datetime.strptime(item_data['d_edit'], '%Y-%m-%d')
                    item = model(**item_data)
                    existing_entry = db.session.query(model).filter_by(**item_data).first()
                    if existing_entry:
                        flash(f'В БД уже есть {existing_entry}')
                    else:

                        try:
                            print(item)
                            db.session.add(item)
                            db.session.commit()
                            flash("Успешно занесено в БД {}.".format(item))

                        except Exception as e:
                            db.session.rollback()
                            flash("Ошибка при сохранении данных: {}".format(str(e)))
                else:
                    flash("Данные {} из JSON файла не соответствуют полям модели {}.".format(item_data, column_names))
            
            return f'Файл {json_file} был прочитан'
        else:
            return "Модель с указанным именем не найдена."  