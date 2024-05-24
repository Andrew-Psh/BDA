# app/routes/data_modification_functions.py

from app import app, db
from app.models import User
from app.forms import AdminUserEditForm, SelectUserToUpdateForm, EditUserForm, RestoreUserFromArchiveForm
from app.decorators import admin_required, active_user_required
from flask import render_template, g, flash, redirect, url_for, jsonify, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
import json
from .helper_functions import convert_value, generate_random_password



@app.route('/select-user-to-update', methods=['GET', 'POST'])
@admin_required
def select_user_to_update():
    # Таблица  "users"
    # Извлечение строковых значений полей из URL для фильтрации запроса к базе данных
    status = 'active'
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

    form = SelectUserToUpdateForm()

    fields_attr = form.to_dict_fields_attr()  
    included_data = {    
                 'status': 'active'
                }
    
    # flash(f"Заполните форму {form.__class__.__name__}!")

    if form.validate_on_submit():
        username = form.user_to_update.input_field.data
       
        if form.send_for_editing.data:
            # flash('Редактирование пользователя')
            return redirect(url_for('edit_user', username=username))

        elif form.send_to_archive.data:
            # Код для кнопки 'В архив'
            user = User.query.filter_by(username=username).first()
            password = generate_random_password(10) 
            user.status = 'archive'
            user.password_hash = generate_password_hash(password)
            
            db.session.commit()
            # flash('Пользователь отправлен в архив')

    return render_template(
                        'admin/select_user_to_update.html', 
                        title="Select user", 
                        form=form, 
                        fields_attr=fields_attr,
                        included_data = json.dumps(included_data),
                        query_filter = table_config_str

    )




@app.route('/restore-user-from-archive', methods=['GET', 'POST'])
@admin_required
def restore_user_from_archive():
# Таблица  "users"
    # Извлечение строковых значений полей из URL для фильтрации запроса к базе данных
    status = 'archive'
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
        "table_label": "Архивные пользователи",
        "model_name": "User",
        "query_conditions_columns": conditions_columns
    }
    # Конфигурация таблицы:
    # - "table_label": Название таблицы
    # - "model_name": Название модели для запросов к базе данных
    # - "query_conditions_columns": Словарь с параметрами для фильтрации запроса: статус пользователя и администраторские права

    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON

    form = RestoreUserFromArchiveForm()

    fields_attr = form.to_dict_fields_attr()  
    included_data = {    
                 'status': 'archive'
                }
    
    # flash(f"Заполните форму {form.__class__.__name__}!")
    messages = ''
    if form.validate():
        if form.submit.data:
            user_name = form.user_to_restore.input_field.data
            # Код для кнопки 'В архив'
            user = User.query.filter_by(username=user_name).first()
            user.status = 'active'
            user.password_hash = generate_password_hash(user_name)  # Имя пользователя (login) является паролем по умолчанию при восстановлении, обновление хэша пароля 

            db.session.commit()
            messages = [f'Пользователь {user_name}  восстановлен из архива.', f'Разовый пароль для входа: {user_name}']

    return render_template(
                        'admin/restore_user_from_archive.html', 
                        title="Restore user", 
                        form=form, 
                        fields_attr=fields_attr,
                        included_data = json.dumps(included_data),
                        query_filter = table_config_str,
                        messages = messages

    )


 
@app.route('/edit-user', methods=['GET', 'POST'])
@admin_required
def edit_user():
    '''Вывод формы редактирования  Пользователей и  таблицы "users" '''

    # Таблица  "users"
    # Извлечение строковых значений полей из URL для фильтрации запроса к базе данных
    status = 'active'
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

    # Конфигурация таблицы:
    table_config  = {
        "table_label": "Пользователи",
        "model_name": "User",
        "query_conditions_columns": conditions_columns
    }

    table_config_str = json.dumps(table_config)  # Преобразование в строку JSON


    # Форма
    form = EditUserForm()
    user_name = request.args.get('username')  # Получение значения переменной user_name из GET запроса
    filter_criteria = {'username': user_name}
    current_record = User.query.filter_by(**filter_criteria).first()        
    fields_attr = form.to_dict_fields_attr()   

    # Заполнение полей формы
    form.original_username = current_record.username
    form.original_email =current_record.email
    form.username.data = current_record.username
    form.email.data = current_record.email
    form.is_admin.data = current_record.is_admin
  
    if form.is_submitted() and form.validate(): 

        if form.submit.data:
            try:
                is_admin_value = request.form.get('is_admin')
                username_value = request.form.get('username')
                email_value = request.form.get('email')
            
                if username_value and form.username.data != username_value:
                    current_record.username = username_value

                if email_value and form.email.data != email_value:
                    current_record.email = email_value

                if not is_admin_value:
                    current_record.is_admin = False

                else:
                    current_record.is_admin = True

                if form.admin_password_reset.data:
                    # Имя пользователя (login) является паролем по умолчанию при сбросе, обновление хэша пароля
                    current_record.password_hash = generate_password_hash(form.username.data) 
            
                db.session.add(current_record)
                db.session.commit()

            except Exception as err:
                db.session.rollback()
                print(f'Error updating user: {str(err)}', 'error')
                raise 
        elif form.cancel.data:
            pass
            # print("Сработала кнопка 'Отменить'")

        return redirect(url_for('select_user_to_update'))
    
    return render_template(
                        'admin/edit_user.html', 
                        title="Select user", 
                        form=form, 
                        fields_attr=fields_attr,
                        query_filter = table_config_str
    )

