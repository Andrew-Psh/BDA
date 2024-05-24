from app import app
from flask import jsonify, render_template, request
from app.models import ModelAccum, Accum, City, Equipment, Node, State, History, User, LogCity, LogUser, LogUpdateUser
import json
from .helper_functions import convert_value

@app.route('/models', methods=['GET', 'POST'])
def get_table_models():
    '''вывод таблицы "models" '''

   # Создание словаря строковых значений полей из URL для фильтрации запроса к базе данных
    conditions_columns = {}
    table_config  = {
        "table_label": "Модели аккумуляторов",
        "model_name": ModelAccum.__name__,
        "query_conditions_columns": conditions_columns
    }
    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON

    link_buttom = 'add_model'
    buttom_name = 'Добавить модель аккумулятора'

    return render_template(
        'common/view_table.html', 
        title = "Models", 
        query_filter = table_config_str,
        buttom_name = buttom_name, 
        link_buttom = link_buttom
    )


@app.route('/accs')
def get_table_accs():
    '''вывод таблицы "accs" '''

    # Создание словаря строковых значений полей из URL для фильтрации запроса к базе данных
    conditions_columns = {}
    table_config  = {
        "table_label": "Аккумуляторы",
        "model_name": Accum.__name__,
        "query_conditions_columns": conditions_columns
    }
    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON

    link_buttom = 'add_accum'
    buttom_name = 'Добавить аккумулятор'

    return render_template(
        'common/view_table.html', 
        title = "Accums", 
        query_filter = table_config_str,
        buttom_name = buttom_name, 
        link_buttom = link_buttom
    )

@app.route('/cities')
def get_table_cities():
    '''вывод таблицы "cities" '''

    # Создание словаря строковых значений полей из URL для фильтрации запроса к базе данных
    # conditions_columns = {}
    table_config  = {
        "table_label": "Города",
        "model_name": City.__name__,
        # "query_conditions_columns": conditions_columns
    }
    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON

    link_buttom = 'add_city'
    buttom_name = 'Добавить Город'

    return render_template(
        'common/view_table.html', 
        title = "Cities", 
        query_filter = table_config_str,
        link_buttom = link_buttom,
        buttom_name = buttom_name
    )


@app.route('/equip')
def get_table_equip():
    '''вывод таблицы equip'''

    # Создание словаря строковых значений полей из URL для фильтрации запроса к базе данных
    conditions_columns = {}
    table_config  = {
        "table_label": '"Оборудование"',
        "model_name": Equipment.__name__,
        "query_conditions_columns": conditions_columns
    }
    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON

    return render_template(
        'common/view_table.html', 
        title = "Equipment", 
        query_filter = table_config_str,
    )


@app.route('/node_srv', methods=['GET', 'POST'])
def get_table_nodes_srv():
    '''вывод таблицы "nodes" '''

     # Создание словаря строковых значений полей из URL для фильтрации запроса к базе данных
    conditions_columns = {}
    table_config  = {
        "table_label": '"Узлы доступа"',
        "model_name": Node.__name__,
        "query_conditions_columns": conditions_columns
    }
    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON

    link_buttom = 'add_node'
    buttom_name = 'Добавить узел связи'

    return render_template(
        'common/view_table.html', 
        query_filter = table_config_str,
        link_buttom = link_buttom, 
        buttom_name = buttom_name
    )


@app.route('/states', methods=['GET', 'POST'])
def get_table_states():
    '''вывод таблицы "states" '''

    # Создание словаря строковых значений полей из URL для фильтрации запроса к базе данных
    conditions_columns = {}
    table_config  = {
        "table_label": '"Статус"',
        "model_name": State.__name__,
        "query_conditions_columns": conditions_columns
    }
    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON

    return render_template(
        'common/view_table.html', 
        title = "States", 
        query_filter = table_config_str
    )
@app.route('/users/', methods=['GET', 'POST'])
def get_table_users():
    '''вывод таблицы "users" '''
   # Извлечение строковых значений полей из URL для фильтрации запроса к базе данных
    status = request.args.get('status')
    is_admin = request.args.get('is_admin')

    # Создание словаря строковых значений полей из URL для фильтрации запроса к базе данных
    conditions_columns = {
        'status': status, 
        'is_admin': is_admin
    }

    # Цикл для конвертации строковых значений в bool
    for field, value in conditions_columns.items():
        if value:            
            conditions_columns[field] = convert_value(value)

    table_config  = {
        "table_label": "Пользователи",
        "model_name": "User",
        "query_conditions_columns": conditions_columns
    }
    # Конфигурация таблицы:
    # - "table_label": Название таблицы
    # - "model_name": Название модели для запросов к базе данных
    # - "query_conditions_columns": Словарь с параметрами для фильтрации запроса: статус пользователя и администраторские права

    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON

    return render_template(
        'common/view_table.html', 
        title = "Users", 
        query_filter = table_config_str
    )


@app.route('/history', methods=['GET', 'POST'])
def get_table_history():
    '''вывод таблицы "history" '''

    # Создание словаря строковых значений полей из URL для фильтрации запроса к базе данных
    conditions_columns = {}
    table_config  = {
        "table_label": '"History"',
        "model_name": History.__name__,
        "query_conditions_columns": conditions_columns
    }
    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON

    return render_template(
        'common/view_table.html', 
        title = "History", 
        query_filter = table_config_str
    )    


@app.route('/log_cities')
def get_table_log_cities():
    '''вывод таблицы "log_cities" '''

     # Создание словаря строковых значений полей из URL для фильтрации запроса к базе данных
    conditions_columns = {}
    table_config  = {
        "table_label": '"История изменений в таблице города"',
        "model_name": LogCity.__name__,
        "query_conditions_columns": conditions_columns
    }
    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON

    link_buttom = 'add_city'
    buttom_name = 'Добавить Город'

    return render_template(
        'common/view_table.html', 
        title = "Log_cities", 
        query_filter = table_config_str,
        link_buttom = link_buttom,
        buttom_name = buttom_name
    )    

@app.route('/log_user', methods=['GET', 'POST'])
def get_table_log_users():
    '''вывод таблицы "log_users" '''

    # Создание словаря строковых значений полей из URL для фильтрации запроса к базе данных
    conditions_columns = {}
    table_config  = {
        "table_label": '"log_users"',
        "model_name": LogUser.__name__,
        "query_conditions_columns": conditions_columns
    }
    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON

    return render_template(
        'common/view_table.html', 
        title = "log_users", 
        query_filter = table_config_str
    )    


@app.route('/log_update_user', methods=['GET', 'POST'])
def get_table_log_update_user():
    '''вывод таблицы "log_update_user" '''

    # Создание словаря строковых значений полей из URL для фильтрации запроса к базе данных
    conditions_columns = {}
    table_config  = {
        "table_label": '"log_update_user"',
        "model_name": LogUpdateUser.__name__,
        "query_conditions_columns": conditions_columns
    }
    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON

    return render_template(
        'common/view_table.html', 
        title = "log_users", 
        query_filter = table_config_str
    )    