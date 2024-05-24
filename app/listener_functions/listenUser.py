# app/listens_models/listener_functions/listenUser.py

from app import db
from sqlalchemy.event import listens_for
from app.models import UserAction, LogUser, LogUpdateUser, User
from flask import flash
from flask_login import current_user
from app.routes.helper_functions import get_users_action_id, mapping_field_and_user_action
from datetime import datetime, timezone


#  Слушатель для отслеживания изменений в SourceTable и их копирования в DestinationTable

print('in app/listens_models/User.py')

field_to_action_mapping = {
    'password': 'Смена пароля',
    'starus': 'Перемещение пользователя в архив',
    'is_admin': 'Изменение статуса администратора'
}
def get_id(record):
    record_id = UserAction.query.filter_by(action=record).with_entities(UserAction.id).scalar()
    print('in get_id, record_id:', record_id)
    return record_id


# Декоратор слушателя событий
@listens_for(User, 'after_insert')
def after_insert_update_delete_listener(mapper, connection, target):
    current_id = current_user.id if current_user.is_authenticated else 1
    new_record = LogUser(
        log_id=target.id,
        log_user=target.username,
        log_email = target.email,
        new_password = True,
        user=current_id,
        user_action=get_users_action_id('Добавление')
    )
    db.session.add(new_record)
    flash(f"В 'log_users' добавлена запись {new_record}")

    
@listens_for(User, 'before_update')
def log_update_user(mapper, connection, target):
    print(User.log_update_user_rel)
    # Получаем доступ к состоянию экземпляра объекта User
    state = target._sa_instance_state

    # Получаем все изменения, которые будут применены при вызове session.commit()
    mapper_changes = state.committed_state

    # Создаем словарь для отслеживания изменений
    changes = {}

    for attr in mapper_changes:
        
        if attr != 'id' and attr != 'log_update_user_rel':
            old_value = mapper_changes[attr]
            new_value = getattr(target, attr)
            if old_value != new_value:
                if attr == 'password_hash':
                   changes[attr] = {
                    'old_value': 'Пароль скрыт',
                    'new_value': 'Пароль скрыт'
                }
                else:
                    changes[attr] = {
                        'old_value': str(old_value),
                        'new_value': str(new_value)
                    }
    if changes:
        for field, values in changes.items():
            log_update = LogUpdateUser(
                user_id=target.id,
                field_changed=field,
                old_value=values['old_value'],
                new_value=values['new_value'],
                action_taken= mapping_field_and_user_action(field), 
                author_id=current_user.id, 
                timestamp=datetime.now(timezone.utc)
            )
            db.session.add(log_update)
