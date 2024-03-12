"""
Файл: app/routes.py
Автор: Андрей Пшеничный
Дата создания: 13 февраля 2024

Описание:
Этот файл содержит маршруты и функции представлений для обработки различных функциональностей в приложении Flask.

Функции:
1. get_model(table_name): Получение модели и атрибута на основе имени таблицы.
2. show_field(): Отображение составной формы с динамическими полями и обработка отправки формы.
3. load_json(): Обработка загрузки JSON данных в базу данных на основе ввода пользователя.
4. show_dinamicselectfield(): Демонстрация динамических полей выбора в форме и обработка отправки формы.

Маршруты:
1. /show-field:
    - Методы: GET, POST
    - Описание: Отображение составной формы с динамическими полями.

2. /load_json:
    - Методы: GET, POST
    - Описание: Обработка загрузки JSON данных на основе ввода пользователя.

3. /show-dinamicselectfield:
    - Методы: GET, POST
    - Описание: Демонстрация динамических полей выбора в форме.

Использование:
1. Обеспечьте правильную валидацию форм и их обработку в каждом маршруте для плавного взаимодействия с пользователем.
2. Поддерживайте однородность во flash-сообщениях, чтобы дать четкую обратную связь пользователям.

Примечание:
- Этот файл служит центральной точкой управления маршрутами и представлениями в приложении Flask.
- Регулярно обновляйте и оптимизируйте функции маршрутов для повышения производительности приложения и опыта пользователя.

"""


from app import app, db
from flask import render_template, url_for, flash, jsonify, request, redirect
from app.models import City, Color, Character, Address
from app.forms import JSONFileForm, DinamicSelectField, AddCharacter
from utilities import load_data_from_json
from jinja2 import Environment, BaseLoader
from flask import Flask, render_template


def get_model(table_name):
    """
    Получает модель и соответствующий ей атрибут на основе предоставленного имени таблицы.

    Параметры:
    - table_name (str): Название таблицы для получения модели и атрибута.

    Возвращает:
    Кортеж, содержащий класс модели и атрибут для запроса указанной таблицы.

    Пример использования:
    get_model('users')

    Пример возврата:
    (User, User.name)
    """
    data = {
        # 'users': {'model': User, 'field': User.name}, 
        # 'colors': {'model': Color, 'field': Color.name},
        # 'addresses': {'model': Address, 'field': Address.location},
        # 'characters': {'model': Character, 'field': Character.name}
        }
    return data[table_name]


@app.route('/get_choices')
def get_choices():
    """
    Извлекает варианты выбора из указанной таблицы в базе данных и возвращает их в формате JSON.

    Параметры:
    - table_name (параметр запроса): Название таблицы, из которой необходимо извлечь варианты выбора.

    Возвращает:
    JSON-ответ, содержащий извлеченные варианты выбора из указанной таблицы.

    Пример использования:
    GET /get_choices?table_name=example_table

    Пример ответа:
    ["column1", "column2", "column3"]
    """

    table_name = request.args.get('table_name')    
    data = db.session.query(get_model(table_name)['field']).all()
    columns = [name[0] for name in data]
    print("columns = ", columns)  # for logging

    return jsonify(columns)


        # @app.route('/show-dinamicselectfield', methods=['GET', 'POST'])
        # def show_dinamicselectfield():
        #     """
        #     Демонстрация использования динамических полей выбора в форме и обработка отправки формы.

        #     Поведение:
        #     - Если форма действительна при отправке, flash-сообщения указывают на ее действительность и отображают 
        #       введенные данные для динамических полей выбора.
        #     - Если форма недействительна, flash-сообщения указывают на то, что форма недействительна, и отображают 
        #       введенные данные для динамических полей выбора.

        #     Возвращает:
        #     Отображает шаблон 'samples/dinamic_select_field.html' с заголовком 'Показать поле' и объектом формы DinamicSelectField.
        #     """
        #     form = DinamicSelectField()
            
        #     if form.validate_on_submit():
        #         flash('Форма валидна')
        #         flash('Введены данные Input - {}; Select - {}.'.format(form.input_field.data, form.selection_from_db.data))
        #     else:
        #         flash('Форма не валидна')
        #         flash('Введены данные Input - {}; Select - {}.'.format(form.input_field.data, form.selection_from_db.data))

        #     return render_template('samples/dinamic_select_field.html', title='Show Field', form=form)




@app.route('/')
@app.route('/index')
def index():
    # return "Hello, World!"
    return render_template('common/index.html', title='Home')


        # @app.route('/add_character', methods=['GET', 'POST'])
        # def add_character():
        #     form = AddCharacter()
        #     # fields_name = form.to_list_field()
        #     fields_data = form.to_dict_field_attr()
            

        #     if form.validate_on_submit(): 
        #         flash(f"Форма {form.__class__.__name__} валидна!")
        #         try:
        #             character_data = form.character_name.data
        #             color_data = form.color_name.input_field.data
        #             address_data = form.address.input_field.data

        #             color_obj = Color.query.filter_by(name=color_data).first()
        #             if not color_obj:
        #                 color_obj = Color(name = color_data)
        #                 db.session.add(color_obj)

        #             address_obj = Address.query.filter_by(location=address_data).first()
        #             if not address_obj:
        #                 address_obj = Address(location = address_data)
        #                 db.session.add(address_obj)

        #             character_obj = Character.query.filter_by(name=character_data).first()
        #             if not character_obj:
        #                 character_obj =Character(name =character_data)
        #                 character_obj.colors.append(color_obj) 
        #                 character_obj.addresses.append(address_obj) 
        #                 db.session.add(character_obj)
        #                 db.session.commit()
                    
        #             flash("Персонаж {} с любимым цветом {} и адресом {} внесен в БД.".format(character_data, color_data, address_data))
        #             return redirect(url_for('add_character'))    
                
        #         except ValueError as e:
        #             flash(f"Произошла ошибка: {e}")
        #             raise ValueError('Пользователь не внесен в БД') 
        
        #     return render_template('add_character.html', 
        #                            title="Add Character", 
        #                            form=form, 
        #                            fields_data=fields_data 
        #                            )



@app.route('/cities', methods=['GET', 'POST'])
def get_table_cities():
    items = City.query.all()
    if items:
        return render_template('from_srv_view_cities.html', title="Cities", items = items)
    return url_for('index')  



##################### U T I L I T E S #####################

@app.route('/load_json', methods=['GET', 'POST'])
def load_json():
    """
    Обработка загрузки JSON данных на основе ввода пользователя с использованием формы.

    Поведение:
    - При действительной форме после отправки:
        - Извлечь имя файла JSON и выбранное имя модели.
        - Загрузить данные в базу данных с помощью 'load_data_from_json(json_file, model)'.
        - Очистить поля формы после успешной отправки.
    - Если форма не прошла проверку:
        - Показать всплывающее сообщение для проверки вводимых данных.
    - Для запросов GET:
        - Отобразить сообщение о вводе данных в форму.

    Возвращает:
    Отображает шаблон 'utilities/json_file_form.html' с заголовком 'Загрузить JSON' и объектом формы JSONFileForm.
    """
    form = JSONFileForm()

    if form.validate_on_submit():
        json_file = form.file.data.filename
        model = form.model_name.data
        loader = load_data_from_json(json_file, model)
        form.file.data = None
        form.model_name.data = None
    elif request.method == 'POST':
        flash('Форма не прошла валидацию. Пожалуйста, проверьте данные.')
    else:
        flash('Пожалуйста, введите данные в форму')

    return render_template('utilites/json_file_form.html', title='Load json', form=form)