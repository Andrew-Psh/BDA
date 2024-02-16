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
from wtforms import Form, SelectField, StringField, SubmitField, FormField, FileField
from wtforms.validators import DataRequired, ValidationError, Length
from werkzeug.utils import secure_filename
from app.models import User, Color


class DinamicSelectField(FlaskForm):
    '''
    Представляет составное поле выбора с динамическим заполнением select_field списком из БД в 
    зависимости от введенного значения в поле input_field
    '''
    input_field = StringField('', validators=[DataRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'Введите значение'})
    selection_from_db = SelectField('', validate_choice=False, choices=[], render_kw={'placeholder': 'Выберите значение'})    

class AddUser(DinamicSelectField):
    """
    Представляет форму для добавления пользователя с несколькими полями.
    """
    user = FormField(DinamicSelectField)
    color = FormField(DinamicSelectField)
    address = StringField('Введите адрес', validators=[DataRequired()], render_kw={'placeholder': 'Введите адрес'})

    submit = SubmitField('Добавить')    

    def to_dict_field_attr(self):
        return {
                'user': {'label': 'Пользователь', 'table_name': 'users'}, 
                'color': {'label': 'Цвет', 'table_name': 'colors'}
                } 
    
    def to_list_field(self):
        return [ 
            {
            'compare_result': self.user.input_field.data == self.user.selection_from_db.data,
            'field_name': self.user.input_field.name,
            'field_data': self.user.input_field.data,
            'table_name': 'users'
            },
            {  
            'compare_result': self.color.input_field.data == self.color.selection_from_db.data,
            'field_name': self.color.input_field.name,
            'field_data': self.color.input_field.data,
            'table_name': 'colors'
            },
            {
            'compare_result': True,
            'field_name': self.address.name,
            'field_data':  self.address.data,
            'table_name': 'addresses'
            }
        ]


##################### U T I L I T E S #####################     


class JSONFileForm(FlaskForm):
    """
    Представляет форму для загрузки данных в формате json в БД.
    """
    # DEFAULT_CHOICE = [('', 'Выбери модель')]  # Значение по умолчанию для model_choices

    model_choices = [('User', 'User'), ('Color', 'Color' )]  # Добавляем DEFAULT_CHOICE к вариантам выбора модели
    # model_choices = [('', 'Выбери  модель'), ('User', 'User'), ('Color', 'Color' )]  # Создание списка вариантов для выбора модели
    
    file = FileField('Выберите JSON файл', validators=[DataRequired()], render_kw={"webkitdirectory": True, "directory": "db_loader_and_json"})
    model_name = SelectField('Выберите модель', choices=[('', 'Выбери модель')] + model_choices, validators=[DataRequired()])  # Добавляем значение по умолчанию к вариантам выбора модели
    submit = SubmitField('Добавить')

    def validate_file(self, file):
        if file.data:           
            print('file.data:', file.data)  # Добавим отладочный вывод
            filename = secure_filename(file.data.filename)
            if not filename.endswith('.json'):
                raise ValidationError('Пожалуйста, выберите файл с расширением .json')
