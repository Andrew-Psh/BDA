from app import app, db
from flask import jsonify, request, abort, g
from app.models import City, Node, ModelAccum, State, Equipment, Accum, History, LogCity
from app.routes import helper_functions
from jinja2 import Environment, BaseLoader
from sqlalchemy.orm import aliased
from app.forms import AdminUserEditForm
import json


#       ############## F O R M - F I E L D ##################   
@app.route('/get_choices')
def get_choices():
    """
    В функции get_choices(): получаем из файла dsf.js переменные model_name  и model_field_name
    с информацией об имени таблицы и колонке в которой будет осуществлен поиск и отбор 
    данных для заполнения динамического поля selection_from_db bp из составной формы DinamicSelectField

    Возвращает:
    данные уникальные записи поля model_field_name из модели model_name в формате json,
 
    Обработка ошибок:
        - Если параметр 'table_field' не был передан в запрос, возвращается код ошибки 400.
        - Если параметр 'table_field' не соответствует формату 'table.field', возвращается код ошибки 400.
        - Если таблица с указанным именем не найдена, возвращается код ошибки 400.
    """
    
    model_name = request.args.get('model_name')
    field = request.args.get('model_field_name') 
    included_data = request.args.get('included_data') # данные для фильтрации запроса
    included_data = json.loads(included_data)
    print('included_data:', included_data)
    if model_name is None:
        print("Параметр 'model_name' не был передан в запрос.")
        abort(400)
    elif field is None:
        print("Параметр 'model_field_name' не был передан в запрос.")
        abort(400)  
    
    
         
    try:  
        model = helper_functions.get_model(model_name)
        if included_data is None:
            data = db.session.query(getattr(model, field)).all()
        else:
            data = db.session.query(getattr(model, field)).filter_by(**included_data).all()
        # data = db.session.query(getattr(model, field)).all()
        # print('in data_request_server.data, SET(DATA) =', set(data)) # Вывод отладочной информации в терминал
        columns = [name[0] for name in data]
        # Убрать повторения из списка columns и вернуть уникальные значения
        unique_columns = list(set(columns))

        # print("in in data_request_server.data, get_choices(): unique_columns = ", unique_columns)  # Вывод отладочной информации в терминал

    except KeyError as err:
        abort(400)


    return jsonify(unique_columns)

@app.route('/get_data_from_db')
def get_data_from_db():
    form_name = request.args.get('form_name') 
    model_name = request.args.get('model_name')
    field = request.args.get('model_field_name') 
    chosen_value = request.args.get('chosen_value')
    filter_criteria = {field: chosen_value}

    form_data = helper_functions.full_form_fields(form_name, model_name, filter_criteria)
    return jsonify(form_data)


#       ############## G R I D J S  ##################   
# получение данных  с сервера GRIDJS
@app.route('/api/data',  methods=['POST'])
def data():
    '''
    Функция data(): получает данные с сервера GRIDJS по заданной таблице.
    В функции data(): получаем из файла gridInitializer.js переменную  table_name запрашиваем 
    из БД соответствующие данные для отображения таблицы.
    Возвращает:
    данные в формате JSON с учетом сортировки, фильтрации, пагинации и общего количества записей.

    '''
    # print("Start app.route('/api/data',  methods=['POST'])")
    data = request.get_json()

    # Получение имени модели и самой модели
    model_name = data['model_name']
    model = helper_functions.get_model(model_name)

    # Получение списка колонок модели
    columns = model.get_columns()

    # Проверка наличия условий фильтрации в запросе
    if 'query_conditions_columns' in data:
        query_conditions = data['query_conditions_columns']

        # Создание списка условий для фильтрации, исключая значения None
        filtered_conditions = {column: value for column, value in query_conditions.items() if value is not None}
        conditions = [getattr(model, column) == value for column, value in filtered_conditions.items()]

        # Применение фильтрации, если есть условия
        if conditions:
            query = model.query.filter(*conditions)
        else:
            query = model.query
    else:
        query = model.query


    # sorting
    sort = request.args.get('sort')
    if sort:
        colomn_list = [item['id'] for item in columns if 'id' in item]
        order = []
        for s in sort.split(','):
            direction = s[0]
            name = s[1:]
            if name not in colomn_list:
                name = 'name'
            col = getattr(model, name)
            if direction == '-':
                col = col.desc()
            order.append(col)
        if order:
            query = query.order_by(*order)


    # search filter
    search = request.args.get('search')
    # print('search:', search) # Вывод отладочной информации в терминал
    if search:
        query = perform_search(model, search)
        # print('query:', query) # Вывод отладочной информации в терминал
    total = query.count()
    # print('total:', total) # Вывод отладочной информации в терминал

    # pagination
    disable_pagination =  False
    start = request.args.get('start', type=int, default=0)
    length = request.args.get('length', type=int, default=10)

    if disable_pagination:
        # В случае отключения пагинации выводить все данные
        query = model.query  # Пример вашего запроса без пагинации
        # print('Pagination disabled, retrieving all data...')
    else:
        # Включение пагинации с параметрами start и length
        if start >= 0 and length >= 0:  # Проверка на неотрицательные значения для начала и длины
            query = query.offset(start).limit(length)
            # print(f'Pagination enabled, retrieving data from position {start} with length {length}...')

    # print('Applied pagination - start:', start, 'length:', length)

    return jsonify({
        'data': [item.to_dict() for item in query],
        'columns': columns,
        'total': total,
    })  

# выполнить поиск в БД для отображение таблиц gridjs
def perform_search(curent_model, search):
    """
    Функция perform_search(current_model, search) выполняет поиск в указанной модели на основе заданного запроса.

    Аргументы:
    current_model (Model): Модель данных для выполнения поиска.
    search (str): Строка запроса для поиска.

    Возвращает:
    results (list): Список результатов поиска.

    Пример использования:
    results = perform_search(ModelAccum, 'search_example')
    """
    if curent_model == Node:

        return  Node.query.join(City, Node.city == City.id).filter(db.or_(
            Node.street.like(f'%{search}%'),
            Node.house.like(f'%{search}%'), 
            Node.place.like(f'%{search}%'),
            City.city.like(f'%{search}%')
        ))
    
    elif curent_model == City:

        return City.query.filter(db.or_(
            City.city.like(f'%{search}%'),
            City.comment.like(f'%{search}%') 
            ))   
    
    elif curent_model == State:

        return  State.query.filter(db.or_(
            State.state.like(f'%{search}%'),
            ))   
    
    elif curent_model == ModelAccum:

        return  ModelAccum.query.filter(db.or_(
            ModelAccum.model.like(f'%{search}%'),
            ModelAccum.manuf.like(f'%{search}%'),
            ModelAccum.charge.like(f'%{search}%')
            ))   
    
    elif curent_model == Equipment:

        return  Equipment.query.filter(db.or_(
            Equipment.type.like(f'%{search}%'),
            ))       

    elif curent_model == Accum:

        return Accum.query \
            .join(ModelAccum, Accum.model == ModelAccum.id) \
            .join(Node, Accum.node == Node.id) \
            .join(State, Accum.state == State.id) \
            .join(Equipment, Accum.equip == Equipment.id) \
            .filter(db.or_(
                ModelAccum.model.like(f'%{search}%'),   
                Node.addr.like(f'%{search}%'),
                State.state.like(f'%{search}%'),
                Equipment.type.like(f'%{search}%'),   
                Accum.No.like(f'%{search}%'),
                Accum.d_prod.like(f'%{search}%'),
                Accum.d_edit.like(f'%{search}%'),
                Accum.comment.like(f'%{search}%'),
            ))   
    
    elif curent_model == History:

        return  History.query.filter(db.or_(
            History.id_rec.like(f'%{search}%'),
            History.acc_id.like(f'%{search}%'),
            History.model.like(f'%{search}%'),
            History.No.like(f'%{search}%'),
            History.d_prod.like(f'%{search}%'),
            History.state.like(f'%{search}%'),
            History.node.like(f'%{search}%'),
            History.equip.like(f'%{search}%'),
            History.d_edit.like(f'%{search}%'),
            History.comment.like(f'%{search}%'),
            History.timestamp.like(f'%{search}%'),
            ))     


@app.route('/update_fields', methods=['POST'])
def update_field():
    field_data = request.json['field_data']

    # Дополнительная обработка данных и сохранение

    return 'Данные успешно получены и обработаны на сервере.'
