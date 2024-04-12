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
from wtforms import Form, SelectField, StringField, SubmitField, FormField, FileField, IntegerField, DateField, PasswordField, BooleanField
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
    

    def to_dict_field_attr(self):
        return {
                'city_name': {'label': 'Город', 'table_field': 'cities.city'},
                } 

class DeleteCity(DinamicSelectField):
    
    city = FormField(DinamicSelectField)

    # city = StringField("Удалить запись из таблицы 'cities'", validators=[Optional(), Length(max=50)], render_kw={'placeholder': 'Удалить запись'})

    submit = SubmitField('Удалить')    
    

    def to_dict_field_attr(self):
        return {
                'city': {'label': 'Город', 'table_field': 'cities.city'},
                } 




class AddNode(DinamicSelectField):
    city_name = FormField(DinamicSelectField)
    street_name = FormField(DinamicSelectField)
    house = StringField('Номер дома', validators=[DataRequired(), Length(max=50)], render_kw={'placeholder': 'Номер дома'})
    place = StringField('Место', validators=[DataRequired(), Length(min=3, max=50)], render_kw={'placeholder': 'Место'})
    comment = StringField('Комментарии', validators=[Optional(), Length(max=50)], render_kw={'placeholder': 'Комментарии'})

    submit = SubmitField('Добавить')    
    

    def to_dict_field_attr(self):
        return {
                'city_name': {'label': 'Город', 'table_field': 'cities.city'},
                'street_name': {'label': 'Улица', 'table_field': 'nodes.street'}
                } 


class AddModel(DinamicSelectField):
    add_model = FormField(DinamicSelectField)
    add_manuf = FormField(DinamicSelectField)
    add_charge = IntegerField('Емкость аккумулятора Ah', validators=[DataRequired()], render_kw={'placeholder': 'Ah'})
    comment = StringField('Комментарии', validators=[Optional(), Length(max=50)], render_kw={'placeholder': 'Комментарии'})

    submit = SubmitField('Добавить')    

    def to_dict_field_attr(self):
        return {
                'add_model': {'label': 'Модель', 'table_field': 'models.model'},
                'add_manuf': {'label': 'Производитель', 'table_field': 'models.manuf'}
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


    def to_dict_field_attr(self):
        return {
                'add_model': {'label': 'Модель', 'table_field': 'models.model'},
                'add_state': {'label': 'Статус', 'table_field': 'states.state'},
                'add_node': {'label': 'Узел связи', 'table_field': 'nodes.addr'},
                'add_equip': {'label': 'Оборудование', 'table_field': 'equip.type'}
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

    submit = SubmitField('Войти')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        # user = db.session.scalar(db.select(User).where(
        #     User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        # user = db.session.scalar(db.select(User).where(
        #     User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class ChangePassword(FlaskForm):
    old_password = PasswordField('Старый пароль',  validators=[DataRequired()])
    password = PasswordField('Новый пароль', validators=[DataRequired()])
    password2 = PasswordField('Подтвердите новый пароль', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Изменить пароль')

    def validate_old_password(self, old_password):
        if not check_password_hash(current_user.password_hash, old_password.data):
            raise ValidationError('Введите действующий пароль.')