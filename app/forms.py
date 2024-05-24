"""
Файл: app/forms.py
Автор: Андрей Пшеничный
Дата создания: 13 февраля 2024

Описание:
Этот модуль содержит классы FlaskForm, представляющие различные структуры форм для обработки форм в приложении Flask.

Классы:
1. DinamicSelectField (FlaskForm):
    - Представляет составное поле выбора, динамически заполняемое из базы данных на основе ввода пользователя.
    - Поля: input_field, selection_from_db

2. AddUser (DinamicSelectField):
    - Представляет форму для добавления пользователя с несколькими полями.
    - Наследует от DinamicSelectField и добавляет поля пользователя, цвета и адреса.
    - Поля: user, color, address, submit
    - Методы: to_dict_field_attr(), to_list_field()

3. JSONFileForm (FlaskForm):
    - Представляет форму для загрузки JSON данных в базу данных.
    - Поля: file, model_name, submit
    - Методы: validate_file()

Использование:
1. Используйте определенные классы форм в представлениях для обработки ввода пользователя и отправки форм.
2. Настройте поведение формы и валидацию по мере необходимости для конкретных требований.

Примечание:
- Модуль структурирует формы Flask для эффективной обработки ввода пользователя и обработки данных.
- Каждый класс формы служит определенной цели для улучшения опыта пользователя и оптимизации обработки данных в приложении.

"""
import sys
sys.path.append('/Users/andrej/Documents/Devel/search_field_application/venv/lib/python3.12/site-packages')

from flask_wtf import FlaskForm
from wtforms import Form, SelectField, StringField, SubmitField, FormField, FileField, IntegerField, DateField, PasswordField, BooleanField, RadioField,  HiddenField  
from wtforms.validators import DataRequired, ValidationError, Length, Optional, Email, EqualTo
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from app import db
from app.models import User


class DinamicSelectField(FlaskForm):
    '''
    Представляет составное поле выбора с динамическим заполнением select_field списком из БД в 
    зависимости от введенного значения в поле input_field
    '''
    input_field = StringField('', validators=[DataRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'Введите значение'})
    selection_from_db = SelectField('', validate_choice=False, choices=[], render_kw={'placeholder': 'Выберите значение'})    

class AddCity(DinamicSelectField):
    city_name = FormField(DinamicSelectField)
    comment = StringField('Комментарии', validators=[Optional(), Length(max=50)], render_kw={'placeholder': 'Комментарии'})

    submit = SubmitField('Добавить')    
    


    def to_dict_fields_attr(self):
        return {
            'city_name': {
                'label': 'Город',
                'model_name': 'City',
                'model_field_name': 'city'
                },
            }
    

class DeleteCity(DinamicSelectField):
    
    city_name = FormField(DinamicSelectField)
    submit = SubmitField('Удалить')    
    
    def to_dict_fields_attr(self):
            return {
                'city_name': {
                    'label': 'Город',
                    'model_name': 'City',
                    'model_field_name': 'city'
                    },
                }

class AddNode(DinamicSelectField):
    city_name = FormField(DinamicSelectField)
    street_name = FormField(DinamicSelectField)
    house = StringField('Номер дома', validators=[DataRequired(), Length(max=50)], render_kw={'placeholder': 'Номер дома'})
    place = StringField('Место', validators=[DataRequired(), Length(min=3, max=50)], render_kw={'placeholder': 'Место'})
    comment = StringField('Комментарии', validators=[Optional(), Length(max=50)], render_kw={'placeholder': 'Комментарии'})

    submit = SubmitField('Добавить')    
    

    def to_dict_fields_attr(self):
        return {
            'city_name': {
                'label': 'Город',
                'model_name': 'City',
                'model_field_name': 'city'
            },
            'street_name': {
                'label': 'Улица',
                'model_name': 'Node',
                'model_field_name': 'street'
            },
        }


class AddModel(DinamicSelectField):
    add_model = FormField(DinamicSelectField)
    add_manuf = FormField(DinamicSelectField)
    add_charge = IntegerField('Емкость аккумулятора Ah', validators=[DataRequired()], render_kw={'placeholder': 'Ah'})
    comment = StringField('Комментарии', validators=[Optional(), Length(max=50)], render_kw={'placeholder': 'Комментарии'})

    submit = SubmitField('Добавить')    

    def to_dict_fields_attr(self):
        return {
                'add_model': {
                        'label': 'Модель',
                        'model_name': 'ModelAccum',
                        'model_field_name': 'model'
                },
                'add_manuf': {
                        'label': 'Производитель',
                        'model_name': 'ModelAccum',
                        'model_field_name': 'manuf'
                },
        } 


class AddAccum(DinamicSelectField):
    add_model = FormField(DinamicSelectField)
    add_No = IntegerField('No', validators=[DataRequired()], render_kw={'placeholder': 'No'})
    add_d_prod = DateField('Дата производства', validators=[DataRequired()])
    add_state = FormField(DinamicSelectField)
    add_node = FormField(DinamicSelectField)
    add_equip = FormField(DinamicSelectField)
    add_d_edit = DateField('Дата редактирования', validators=[DataRequired()])
    comment = StringField('Комментарии', validators=[Optional(), Length(max=50)], render_kw={'placeholder': 'Комментарии'})

    submit = SubmitField('Добавить')    


    def validate_add_model(self, field):
        if self.add_model.input_field.data not in [choice[0] for choice in field.selection_from_db.choices]:
            raise ValidationError('Выбранное значение не существует в базе данных')

    def to_dict_fields_attr(self):
        return {
                'add_model': {
                            'label': 'Модель',
                            'model_name': 'ModelAccum',
                            'model_field_name': 'model'
                    },
                    'add_state': {
                            'label': 'Состояние',
                            'model_name': 'State',
                            'model_field_name': 'state'
                    },
                    'add_node': {
                            'label': 'Узел связи',
                            'model_name': 'Node',
                            'model_field_name': 'addr'
                    },
                    'add_equip': {
                            'label': 'Оборудование',
                            'model_name': 'Equipment',
                            'model_field_name': 'type'
                    },
                } 
 
class ConfirmationForm(FlaskForm):
    submit_confirm = SubmitField('Подтвердить')
    submit_cancel = SubmitField('Отменить')

class LoginForm(FlaskForm):
    username = StringField('Введите имя', validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class UserRegistrationForm(FlaskForm):
    username = StringField('Введите имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    password2 = PasswordField('Подтвердите  пароль', validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField('Администратор')

    submit = SubmitField('Создать пользователя')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        # user = db.session.scalar(db.select(User).where(
        #     User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_is_admin(self, is_admin):
        is_admin_value = is_admin.data  # Получаем фактическое значение is_admin из формы
        if is_admin.data:
            if current_user.is_anonymous:
                is_admin_exists = User.query.filter_by(is_admin=True, is_active=True).first()
                if is_admin_exists:
                    raise ValidationError(f'Уже есть активные администраторы в системе, доступ к установке статуса администратора ограничен (is_admin: {is_admin.data})')
            elif current_user.is_admin:
                pass
            else:
                raise ValidationError(f'У вас недостаточно прав доступа для изменения статуса администратора ({self.username} is_admin: {is_admin.data})')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        # user = db.session.scalar(db.select(User).where(
        #     User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class ChangePassword(FlaskForm):
    old_password = PasswordField('Старый пароль',  validators=[DataRequired()])
    password = PasswordField('Новый пароль', validators=[DataRequired()])
    password2 = PasswordField('Подтвердите новый пароль', validators=[DataRequired()]) # validators=[DataRequired(), EqualTo('password')]

    submit = SubmitField('Изменить пароль')

    def validate_old_password(self, old_password):
        if not check_password_hash(current_user.password_hash, old_password.data):
            raise ValidationError('Введите действующий пароль.')
        
 
class AdminUserEditForm(DinamicSelectField):
    username = FormField(DinamicSelectField) 
    user_id = StringField('ID', validators=[DataRequired()])
    new_username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    status =  RadioField('Выберите опцию:', choices= [('archive', 'Архив'), ('active', 'Активный пользователь')], default='active')
    is_admin = BooleanField('Администратор', default=False)
    admin_password_reset = BooleanField('Сброс пароля')
    autocomplete = 'disabled'
    
    submit = SubmitField('Применить')
    cancel = SubmitField('Отменить')    

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        # user = db.session.scalar(db.select(User).where(
        #     User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
    def validate_new_username(self, new_username):
        user = User.query.filter_by(username=new_username.data).first()
        # user = db.session.scalar(db.select(User).where(
        #     User.username == new_usename.data))
        if user is not None:
            raise ValidationError('Please use a different usename.')
       
    def to_dict_fields_attr(self):
        return {
                'username': {
                    'label': 'Выбрать пользователя', 
                    'model_name': User.__name__, 
                    'model_field_name': 'username' 
                },
        } 

class AdminUserEditForm(DinamicSelectField):
    username = FormField(DinamicSelectField) 
    user_id = StringField('ID', validators=[DataRequired()])
    new_username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    status =  RadioField('Выберите опцию:', choices= [('archive', 'Архив'), ('active', 'Активный пользователь')], default='active')
    is_admin = BooleanField('Администратор', default=False)
    admin_password_reset = BooleanField('Сброс пароля')
    autocomplete = 'disabled'
    
    submit = SubmitField('Применить')
    cancel = SubmitField('Отменить')    

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        # user = db.session.scalar(db.select(User).where(
        #     User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
    
    def validate_new_username(self, new_username):
        user = User.query.filter_by(username=new_username.data).first()
        # user = db.session.scalar(db.select(User).where(
        #     User.username == new_usename.data))
        if user is not None:
            raise ValidationError('Please use a different usename.')
       
    def to_dict_fields_attr(self):
        return {
                'username': {
                    'label': 'Выбрать пользователя', 
                    'model_name': User.__name__, 
                    'model_field_name': 'username' 
                },
        } 


class SelectUserToUpdateForm(DinamicSelectField):
    user_to_update = FormField(DinamicSelectField) 
    send_for_editing = SubmitField('Редактировать')
    send_to_archive = SubmitField('В архив')

    def to_dict_fields_attr(self):
        return {
                'user_to_update': {
                    'label': 'Выбрать пользователя', 
                    'model_name': User.__name__, 
                    'model_field_name': 'username' 
                },
        } 
class RestoreUserFromArchiveForm(DinamicSelectField):
    user_to_restore = FormField(DinamicSelectField) 
    submit = SubmitField('восстановить из архива')
    cancel = SubmitField('Отменить')    
    def to_dict_fields_attr(self):
        return {
                'user_to_restore': {
                    'label': 'Выбрать пользователя', 
                    'model_name': User.__name__, 
                    'model_field_name': 'username' 
                },
        } 
    
class EditUserForm(FlaskForm):
    original_username = HiddenField()  # Поле для хранения начального логина пользователя
    original_email = HiddenField()  # Поле для хранения начального email пользователя
    # original_is_admin = HiddenField() 
    # original_admin_password_reset = HiddenField() 

    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    status =  RadioField('Выберите опцию:', choices= [('archive', 'Архив'), ('active', 'Активный пользователь')], default='active')
    is_admin = BooleanField('Администратор', default=False)
    admin_password_reset = BooleanField('Сброс пароля')
    autocomplete = 'disabled'
    submit = SubmitField('Применить')
    cancel = SubmitField('Отменить')    

    def validate_form(self):

        if not super(EditUserForm, self).validate():
            """ метод проверяет, прошла ли форма валидацию с помощью метода validate()
                из родительского класса формы (super(EditUserForm, self).validate()). 
                Если форма не прошла валидацию, метод возвращает False.
            """
            return False
        
        username = self.username.data
        print('Проверка валидности формы StringField')
        print(' self.username.data',  self.username.data)
        print('self.original_username.data:', self.original_username.data)
        email = self.email.data
        # is_admin = self.is_admin.data
        # admin_password_reset = self.admin_password_reset.data
        if username != self.original_username.data:
            user = User.query.filter_by(username=username).first()
            if user is not None:
                self.username.errors.append('Please use a different username.')
                return False

        if email != self.original_email.data:
            user = User.query.filter_by(email=email).first()
            if user is not None:
                self.email.errors.append('Please use a different email address.')
                return False
            
        return True
       
    def to_dict_fields_attr(self):
        return {
                'username': {
                    'label': 'Выбрать пользователя', 
                    'model_name': User.__name__, 
                    'model_field_name': 'username' 
                },
        } 