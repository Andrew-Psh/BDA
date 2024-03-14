# utilities/damp_data_to_json.py

"""
Скрипт для преобразования данных в формат JSON и сохранения их в JSON файлы.

Dependencies:
    - json
    - damp_data (модуль с данными)
    - os

Variables:
    json_dir (str): Путь к директории для хранения JSON файлов.
    files (list): Список данных для преобразования.

Steps:
1. Создание директории 'json_files' для хранения JSON файлов.
2. Преобразование данных в формат JSON и сохранение каждого файла данных.
3. Вывод успешного завершения операции.

"""

import json
from datetime import datetime
from damp_data import cities, nodes, equip, models, states, accs, history
import os

# Устанавливаем путь к директории json_files
json_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'json_files')
os.makedirs(json_dir, exist_ok=True)  # Создаем директорию, если ее нет

files = [cities, nodes, equip, models, states, accs, history]

for file in files:
    json_data = json.dumps([{file.fields[i]: item[i] for i in range(1, len(file.fields))} for item in file.data], indent=4, ensure_ascii=False)
    
    # Путь к файлу JSON
    json_path = os.path.join(json_dir, f'{file.table}.json')
    
    # Запись данных в файл
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)
    
    print("Данные успешно преобразованы и сохранены в файл", f'{file.table}.json.')

print("Файлы JSON были сохранены в директории 'json_files'.")
