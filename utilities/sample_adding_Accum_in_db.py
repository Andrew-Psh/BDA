from app import db
from datetime import datetime
import json
from app.models import Accum


# Чтение данных из файла JSON
with open('your_data.json', 'r') as file:
    data = json.load(file)

# Обновление данных существующего аккумулятора или добавление нового
for item in data:
    existing_accum = Accum.query.filter_by(model=item['model'], No=item['No']).first()
    if existing_accum:
        # Если аккумулятор существует, обновляем все необходимые поля, включая инкрементальное добавление новых значений в поле 'equip'
        existing_accum.equip.append(item['equip'])
        existing_accum.node = item['node']
        existing_accum.state = item['state']
        existing_accum.d_prod = item['d_prod']
        existing_accum.d_edit = item['d_edit']
        existing_accum.comment = item['comment']
    else:
        # Если аккумулятор не существует, создаем новый объект для добавления
        # new_accum = Accum(
        #     model=item['model'],
        #     No=item['No'],
        #     d_prod=item['d_prod'],
        #     state=item['state'],
        #     node=item['node'],
        #     equip=[item['equip']],  # Создаем список с одним значением
        #     d_edit=item['d_edit'],
        #     comment=item['comment']
        # )
        # db.session.add(new_accum)
        # Создание новой записи

        new_data_item = Accum()
        for key, value in item.items():
            if hasattr(new_data_item, key):
                if key == 'equip':
                    setattr(new_data_item, key, [value])  # Создание списка с одним значением в поле 'equip'
                elif key in ('d_prod', 'd_edit'):
                    # Преобразование текста в дату для полей 'd_prod' и 'd_edit'
                    try:
                        setattr(new_data_item, key, datetime.strptime(value, '%Y-%m-%d %H:%M:%S'))
                    except ValueError:
                        setattr(new_data_item, key, None)  # Установка None в случае неудачного преобразования
                else:
                    setattr(new_data_item, key, value)

        db.session.add(new_data_item)


# Сохранение изменений в базе данных
db.session.commit()

for key, value in item.items():
            if hasattr(new_data_item, key):
                if key in ['equip']:
                    setattr(new_data_item, key, [value])  # надо добавить значение в поле  'equip'
                else:
                    setattr(new_data_item, key, value)
            db.session.add(new_data_item)
            

for item in data:
    existing_accum = Accum.query.filter_by(model=item['model'], No=item['No']).first()
    if existing_accum:
        for key, value in item.items():
            if hasattr(existing_accum, key):
                if key == 'equip' and value not in existing_accum.equip:
                    existing_accum.equip.append(value)  # Добавление нового значения в список в поле 'equip'
                else:
                    setattr(existing_accum, key, value)  # Обновление других полей

        # Вместо db.session.add(new_data_item) переместите db.session.add(existing_accum) вне цикла
        db.session.add(existing_accum)
