# app/listens_models/listener_functions/listenCity.py

from app import db
from sqlalchemy.event import listens_for
from app.models import UserAction, LogCity, City
from flask import flash
from flask_login import current_user, login_required

#  Слушатель для отслеживания изменений в SourceTable и их копирования в DestinationTable

def get_id(record):
    record_id = UserAction.query.filter_by(action=record).with_entities(UserAction.id).scalar()
    print('in get_id, record_id:', record_id)
    return record_id


print('in app/listens_models/City.py')
@login_required  # Данный декоратор требует аутентификации пользователя
@listens_for(City, 'after_insert')
def after_insert_update_delete_listener(mapper, connection, target):
    if current_user.is_authenticated:
        current_id = current_user.id
    new_record = LogCity(
        log_id = target.id,
        log_city = target.city,
        log_comment = target.comment,
        user = current_id,
        user_action = get_id('Добавление')
        )
    db.session.add(new_record)
    flash(f"В лог БД добавлена запись {new_record} об изменении таблицы 'sities' ")


@listens_for(City, 'after_update')
@login_required  # Данный декоратор требует аутентификации пользователя
def after_insert_update_delete_listener(mapper, connection, target):
    if current_user.is_authenticated:
        current_id = current_user.id

    new_record = LogCity(
        log_id = target.id,
        log_city = target.city,
        log_comment = target.comment,
        user = current_id,
        user_action = get_id('Изменение')
        )
    db.session.add(new_record)
    flash(f"В лог БД добавлена запись {new_record} об изменении таблицы 'sities' ")


@listens_for(City, 'after_delete')
@login_required  # Данный декоратор требует аутентификации пользователя
def after_insert_update_delete_listener(mapper, connection, target):
    if current_user.is_authenticated:
        current_id = current_user.id

    new_record = LogCity(
        log_id = target.id,
        log_city = target.city,
        log_comment = target.comment,
        user = current_id,
        user_action = get_id('Удаление')
        )
    db.session.add(new_record)
    flash(f"В лог БД добавлена запись {new_record} об изменении таблицы 'sities' ")
