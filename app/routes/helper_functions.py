# app/routes/filling_out_forms_data.py

from app.models import City, Node, ModelAccum, State, Equipment, Accum, User, History, LogCity, LogUser, LogUpdateUser, UserAction
import secrets
import string


def generate_random_password(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password

def get_users_action_id(record):
    record_id = UserAction.query.filter_by(action=record).with_entities(UserAction.id).scalar()
    print('in get_id, record_id:', record_id)
    return record_id

def mapping_field_and_user_action(field):
    try:
        user_actions = {   
            'username': 'Редактирование логина',
            'email': 'Смена Email',
            'password_hash': 'Смена пароля',
            'is_admin': 'Изменение роли администратора',
            'status': 'Изменение статуса пользователя'
        }
        user_action = user_actions[field]
    except:
        user_action =  "Действие не определено"
    return get_users_action_id(user_action)


def get_model(model_name):
    """
    Функция get_model(table_name) возвращает модель данных, соответствующую указанному названию таблицы.

    Аргументы:
    table_name  (str): Название таблицы, для которой нужно получить модель данных.

    Возвращает:
    data[table_name] (Model): Модель данных, соответствующая указанному названию таблицы.

    Исключения:
    KeyError: Возникает, если указанное название таблицы отсутствует в словаре data.

    Пример использования:
    get_model('City') # Возвращает модель City

    """

    try:
        data = {
            'City': City, 
            'Node':  Node,
            'ModelAccum': ModelAccum,
            'State': State,
            'Equipment': Equipment,
            'Accum':  Accum,
            'History': History,
            'LogCity': LogCity,
            'User': User,
            'LogUser': LogUser,
            'LogUpdateUser': LogUpdateUser,

            }
        
        return data[model_name]
    
    except KeyError as err:
        error_message = f"KeyError!!! Ключ '{model_name}' словаря 'data' в data функции get_model(model_name) не найден. Mодель не получена."
        print(error_message)
        raise err(error_message)
    

def convert_value(value):
    if value.lower() in ['true', 'false']:
        return value.lower() == 'true'
    elif value.isdigit():
        return int(value)
    else:
        return value
    

def full_form_fields(form_name, model_name, filter_criteria):
    model = get_model(model_name)
    current_record = model.query.filter_by(**filter_criteria).first()        
    filling_out_forms_data = {
        'EditUserForm': {
                'original_username': current_record.username,
                'new_username': current_record.username,
                'original_email': current_record.email,
                'email': current_record.email,
                'is_admin': current_record.is_admin,
                }
        }
    return filling_out_forms_data[form_name]

def is_user_active(user_name: str) -> bool:
    user = User.query.filter_by(username=user_name).first()
    return user.status == 'active'