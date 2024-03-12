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
from wtforms import Form, SelectField, StringField, SubmitField, FormField, FileField, IntegerField, DateField
from wtforms.validators import DataRequired, ValidationError, Length
from werkzeug.utils import secure_filename
from app.models import Character


class DinamicSelectField(FlaskForm):
    '''
    Представляет составное поле выбора с динамическим заполнением select_field списком из БД в 
    зависимости от введенного значения в поле input_field
    '''
    input_field = StringField('', validators=[DataRequired(), Length(min=2, max=50)], render_kw={'placeholder': 'Введите значение'})
    selection_from_db = SelectField('', validate_choice=False, choices=[], render_kw={'placeholder': 'Выберите значение'})    



class AddCharacter(DinamicSelectField):
    character_name = StringField('Введите персонаж', validators=[DataRequired(), Length(min=3, max=50)], render_kw={'placeholder': 'Введите персонаж'})
    color_name = FormField(DinamicSelectField)
    address =  FormField(DinamicSelectField)

    submit = SubmitField('Добавить')    

    def validate_name(self, field):
        existing_character = Character.query.filter_by(name=field.data).first()
        if existing_character is not None:
            raise ValidationError('Такое имя персонажа уже существует в базе данных. Введите другое имя.')

    def to_dict_field_attr(self):
        return {
                'color_name': {'label': 'Цвет', 'table_name': 'colors'},
                'address': {'label': 'Адрес', 'table_name': 'addresses'}
                } 
#####################  #####################     

class CityForm(FlaskForm):
    
    choose_city = SelectField('City', choices=[], coerce=int)
    # base_choose_city = SelectFieldBase('Base choose', )
    comment = StringField('comment', validators=[DataRequired()])

    submit = SubmitField('Sign In')

class EquipmentForm(FlaskForm):  # в разработке
    name = StringField('Equipment', validators=[DataRequired()])      
    submit = SubmitField('Sign In')




# class AccForm(FlaskForm):    
#     id = IntegerField('id', validators=[DataRequired()])
#     model = SelectField('', validators=[DataRequired()])
#     search_model = SearchField('Модель', validators=[DataRequired()])
#     No = StringField('No', validators=[DataRequired()])
#     d_prod = DateField('Дата продажи', validators=[DataRequired()])
#     accum_state = IntegerField('Статус')
#     node = IntegerField('Узел доступа', validators=[DataRequired()])
#     equip = IntegerField('Оборудование')
#     d_edit = DateField()
#     comment = StringField('comment', validators=[DataRequired()])

#     submit = SubmitField('Добавить')



class StatesForm(FlaskForm):
    accum_state = StringField('accum_state', validators=[DataRequired()])
    comment = StringField('comment', validators=[DataRequired()])
    submit = SubmitField('Sign In')

    
class AccForm(FlaskForm):    
    id = IntegerField('id', validators=[DataRequired()])
    model = StringField('model', validators=[DataRequired()])
    No = StringField('No', validators=[DataRequired()])
    d_prod = DateField()
    accum_state = IntegerField('accum_state')
    node = IntegerField('node', validators=[DataRequired()])
    equip = IntegerField('equip')
    d_edit = DateField()
    comment = StringField('comment', validators=[DataRequired()])

    submit = SubmitField('Sign In')


#####################  #####################     


    

##################### U T I L I T E S #####################     


class JSONFileForm(FlaskForm):
    """
    Представляет форму для загрузки данных в формате json в БД.
    """
    # DEFAULT_CHOICE = [('', 'Выбери модель')]  # Значение по умолчанию для model_choices

    model_choices = [('User', 'User'), ('Color', 'Color'), ('Character', 'Character')]  # Добавляем DEFAULT_CHOICE к вариантам выбора модели
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

