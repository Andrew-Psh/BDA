# app/listener_functions/history_handlers.py

from app import db
from sqlalchemy.event import listens_for
from app.models import ModelAccum, History

@listens_for(ModelAccum, 'after_update')  # Устанавливаем слушателя для модели ModelAccum на событие 'after_update'
def after_update_listener(mapper, connection, model):
    # Функция, которая будет выполнена после обновления объекта ModelAccum
    # Получаем данные из модели ModelAccum и создаем новую запись в таблице History
    history_record = History(
        acc_id=model.id,
        model=model.model,
        d_prod=model.d_prod,
        state=model.state,
        node=model.node,
        equip=model.equip,
        d_edit=model.d_edit,
        comment=model.comment
    )
    db.session.add(history_record)  # Добавляем созданную запись в сессию БД
    db.session.commit()  # Сохраняем изменения (делаем коммит) в базе данных