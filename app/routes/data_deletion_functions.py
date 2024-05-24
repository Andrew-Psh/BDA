from app import app, db
from flask import render_template, url_for, flash, redirect
from app.models import City
from app.forms import  DeleteCity, ConfirmationForm
# from jinja2 import Environment, BaseLoader
# from sqlalchemy.event import listens_for
import inspect
from app.routes.helper_functions import get_model
import json


@app.route('/delete_city', methods=['GET', 'POST'])
def delete_city():


    '''вывод формы "DeleteCity" '''

    # вывод таблицы "cities"

    table_config  = {
        "table_label": "Города",
        "model_name": City.__name__,
        # "query_conditions_columns": conditions_columns
    }
    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON


    redirect_to_function = 'get_table_log_cities' # inspect.currentframe().f_code.co_name 
    form = DeleteCity()
    fields_attr = form.to_dict_fields_attr()    
    flash(f"Заполните форму {form.__class__.__name__}!")

    if form.validate_on_submit(): 
        flash(f"Форма {form.__class__.__name__} валидна!")
        choise_field = form.city_name.input_field.data
        model = City
        if choise_field:
            record = City.query.filter_by(city=choise_field).first()
            # Список кортежей с парами "название поля - значение"
            # fields_values = [(column.name, getattr(record, column.name)) for column in record.__table__.columns]
            if record:
                record_id = record.id 
                # record_id = model.query.filter_by(my_data=choise_field).with_entities(model.id).scalar()
                model_name = model.__name__
                flash(f'id: {record_id}, type(record_id): {type(record_id)}')
                return redirect(url_for('confirmation_form', model_name=model_name, record_id=record_id, redirect_to_function=redirect_to_function ))
                    # return redirect(url_for('delete_confirmation', table_name=table_name, record_id=record_id))

            else:
                flash(f"Запись {choise_field} не была найдена")
    

    return render_template('forms/delete_city.html', 
                            title="Delete City", 
                            form=form, 
                            fields_attr=fields_attr,
                            link_insert_data = 'insert_data',
                            lable_insert_data = 'Добавить запись в БД',
                            link_view_data = 'view_data',
                            lable_view_data = 'Посмотреть записи в таблице "cities"',
                            link_view_log = 'view_log',
                            lable_view_log = 'Посмотреть лог БД',    
                            query_filter = table_config_str

    )


@app.route('/confirmation_form/<model_name>/<int:record_id>/<redirect_to_function>', methods=['GET', 'POST'])
def confirmation_form(model_name, record_id, redirect_to_function):
    form = ConfirmationForm()
    flash(f'in confirmation_form! table_name: {model_name}, record_id: {record_id},  redirect_to_function: {redirect_to_function}')
    model = get_model(model_name)
    record = model.query.get(record_id)
    if record:
        record_dict = record.to_dict()

        field_value_pairs = [(str(key) + ": ", str(value) + ",") for key, value in record_dict.items()]
    else:
        # Обработка случая, когда запись с указанным record_id не найдена
        return "Запись не найдена"


    if form.validate_on_submit():
        if form.submit_confirm.data:
            flash('Нажата кнопка "Подтвердить"')
            db.session.delete(record)  # Удаляем запись
            db.session.commit()  # Применяем изменения в БД
            flash(f'Запись {record} успешно удалена')
            return redirect(url_for('delete_city'))
        elif form.submit_cancel.data:
            flash('Нажата кнопка "Отменить"')
            return redirect(url_for('delete_city'))

    return render_template('forms/confirmation_form.html', form=form, field_value_pairs=field_value_pairs)