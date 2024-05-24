from app import app
from flask import jsonify, render_template
from app.models import ModelAccum, Accum, City, Equipment, Node, State, History, User, LogCity


@app.route('/models', methods=['GET', 'POST'])
def get_table_models():
    '''вывод таблицы "models" '''

    model = ModelAccum
    items = model.query.all()
    link_buttom = 'add_model'
    buttom_name = 'Добавить модель аккумулятора'

    return render_template(
        'common/view_table.html', 
        title = "Models", 
        items = items, 
        table_name = '"Моделиаккумуляторов"', # Unicode символ пробела \u00A0 
        key = model.__tablename__, 
        buttom_name = buttom_name, 
        link_buttom = link_buttom
    )


@app.route('/accs', methods=['GET', 'POST'])
def get_table_accs():
    '''вывод таблицы "accs" '''

    model = Accum
    items = model.query.all()
    link_buttom = 'add_accum'
    buttom_name = 'Добавить аккумулятор'

    return render_template(
        'common/view_table.html', 
        title = "Accums", 
        items = items, 
        table_name = '"Аккумуляторы"', 
        key = model.__tablename__, 
        buttom_name = buttom_name, 
        link_buttom = link_buttom
    )

@app.route('/cities')
def get_table_cities():
    '''вывод таблицы "cities" '''
    model = City
    items = model.query.all()
    link_buttom = 'add_city'
    buttom_name = 'Добавить Город'

    return render_template(
        'common/view_table.html', 
        title = "Cities", 
        items = items, 
        table_name = '"Города"', 
        key = model.__tablename__,
        link_buttom = link_buttom,
        buttom_name = buttom_name
    )


@app.route('/equip')
def get_table_equip():
    '''вывод таблицы equip'''

    model = Equipment
    items = model.query.all()

    return render_template(
        'common/view_table.html', 
        title = "Equipment", 
        items = items, 
        table_name = '"Оборудование"', 
        key = model.__tablename__
    )


@app.route('/node_srv', methods=['GET', 'POST'])
def get_table_nodes_srv():
    '''вывод таблицы "nodes" '''

    model = Node
    items = model.query.all()
    link_buttom = 'add_node'
    buttom_name = 'Добавить узел связи'

    return render_template(
        'common/view_table.html', 
        title = "Nodes", 
        items = items, 
        link_buttom = link_buttom, 
        buttom_name = buttom_name, 
        table_name = '"Узлы\u00A0доступа"', # Unicode символ пробела \u00A0 
        key = model.__tablename__
    )


@app.route('/states', methods=['GET', 'POST'])
def get_table_states():
    '''вывод таблицы "states" '''

    model = State
    items = model.query.all()
    return render_template(
        'common/view_table.html', 
        title = "States", 
        items = items, 
        table_name = '"Статус"', 
        key = model.__tablename__
    )



@app.route('/users', methods=['GET', 'POST'])
def get_table_active_users():
    '''вывод таблицы "users" '''

    model = User
    query_filter = '{"column": "is_active", "value": true}'
    print("in get_table_active_users. Значение query_filter:", query_filter)
    # query_filter = jsonify(query_filter)

    return render_template(
        'common/view_table.html', 
        title = "Users", 
        query_filter = query_filter,
        table_name = '"Пользователи"', 
        key = model.__tablename__
    )


@app.route('/history', methods=['GET', 'POST'])
def get_table_history():
    '''вывод таблицы "history" '''

    model = History
    items = model.query.all()

    return render_template(
        'common/view_table.html', 
        title = "History", 
        items = items, 
        table_name = '"История"', 
        key = model.__tablename__
    )


@app.route('/log_cities')
def get_table_log_cities():
    '''вывод таблицы "log_cities" '''
    model = LogCity
    items = model.query.all()

    link_buttom = 'add_city'
    buttom_name = 'Добавить Город'

    return render_template(
        'common/view_table.html', 
        title = "Log_cities", 
        items = items, 
        table_name = '"История\u00A0изменений\u00A0в\u00A0таблице\u00A0города"', 
        key = model.__tablename__,
        link_buttom = link_buttom,
        buttom_name = buttom_name
    )