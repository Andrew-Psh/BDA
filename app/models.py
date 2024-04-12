# app/models.py

from app import db, login
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class City(db.Model):
    '''Модель таблицы `cities` 
    '''
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False, default='0')
    comment =db.Column(db.String(50))

    nodes_rel = db.relationship('Node', 
                                back_populates="city_rel", 
                                uselist=True, 
                                lazy='select'
                                )  # связь на уровне моделей много nodes

    def __repr__(self):
        return f"<Модель 'City': \
            __tablename__ {self.__tablename__}, \
            id {self.id}, \
            city {self.city}, \
            comment {self.comment}>"

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'comment': self.comment,
            # 'nodes': [node for node in self.nodes_rel.all()]
        }
    def get_columns():
      return [
            { 'id': "id", 'name': "id", 'hidden': True },
            { 'id': "city", 'name': "Город", 'sort': True  },
            { 'id': "comment", 'name': "Комментарии", 'sort': False }
            ]
    

class Node(db.Model):
    '''Модель таблицы `nodes` (узлы)
    '''
    __tablename__ = 'nodes'
    
    id = db.Column(db.Integer, primary_key=True)
    addr = db.Column(db.String(50))
    city = db.Column(db.Integer, db.ForeignKey("cities.id"), default=1)
    street =db.Column(db.String(50), default='0')
    house =db.Column(db.String(50))
    place =db.Column(db.String(50))
    comment =db.Column(db.String(50))

    city_rel = db.relationship('City', 
                               back_populates="nodes_rel", 
                               uselist=False
                               )  # ONE city_rel
    
    accums_rel = db.relationship('Accum', 
                                 back_populates="node_rel", 
                                 uselist=True, 
                                 )  # MANY accums_rel
  
    def __repr__(self):
        return f"<Модель 'Node': __tablename__ {self.__tablename__}, id {self.id}, addr {self.addr}, city {self.city_rel.city}, comment {self.comment}, street {self.street}, house {self.house}, place {self.place}>"
  
    def to_dict(self):
        return {
            'id': self.id,
            'addr': self.addr,
            'city': self.city_rel.city,
            'street': self.street,
            'house': self.house,
            'place': self.place,
            'comment': self.comment
        }
    def get_columns():
      return [
            { 'id': "id", 'name': "id", 'hidden': True },
            { 'id': "city", 'name': "Город" },
            { 'id': "addr", 'name': "Адрес", 'hidden': True  },
            { 'id': "street", 'name': "Улица" },
            { 'id': "house", 'name': "Дом" },
            { 'id': "place", 'name': "Место" },
            { 'id': "comment", 'name': "Комментарии", 'sort': False }
            ]
class Accum(db.Model):
    '''
    Модель таблицы accs (аккумуляторы)
    '''    
    __tablename__ = 'accs'
    
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.Integer,  db.ForeignKey("models.id"), default=0)
    No = db.Column(db.String(50))
    d_prod = db.Column(db.DateTime, index=True)
    state = db.Column(db.Integer, db.ForeignKey("states.id"))
    node = db.Column(db.Integer,  db.ForeignKey("nodes.id"), default=0)
    equip = db.Column(db.Integer, db.ForeignKey("equip.id"))
    d_edit = db.Column(db.DateTime, index=True)
    comment = db.Column(db.String(50))

    model_rel = db.relationship('ModelAccum', 
                                back_populates = 'accums_rel', 
                                cascade="save-update",
                                uselist=False, 
                                )  # связь на уровне моделей ONE model
    node_rel = db.relationship('Node', 
                               back_populates = 'accums_rel', 
                               cascade="save-update", 
                               uselist=False, 
                               )  # связь на уровне моделей ONE node

    states_rel = db.relationship("State", 
                                back_populates="accums_rel", 
                                cascade="save-update", 
                                uselist=False, 
                                ) 

    equips_rel = db.relationship('Equipment', 
                                 back_populates="accum_rel", 
                                 cascade="save-update", 
                                 uselist=False, 
                                 )  # связь на уровне моделей один accum

    def __repr__(self):
        return f"<Модель 'Accum': \
                    __tablename__ {self.__tablename__}, \
                    id {self.id}, \
                    model {self.model}, \
                    No {self.No}, \
                    d_prod {self.d_prod}, \
                    state {self.state}, \
                    node {self.node}, \
                    equip {self.equip}, \
                    d_edit {self.d_edit}, \
                    comment {self.comment}>"
    def to_dict(self):
        return {
            'id': self.id,
            'model': self.model_rel.model, 
            'No': self.No, 
            'd_prod': self.d_prod, 
            'state': self.states_rel.state, 
            'node': self.node_rel.addr, 
            'equip': self.equips_rel.type, 
            'd_edit': self.d_edit, 
            'comment': self.comment
        }
    def get_columns():
      return [
            { 'id': "id", 'name': "id", 'hidden': True },
            { 'id': "model", 'name': "Модель" },
            { 'id': "No", 'name': "No", 'hidden': True  },
            { 'id': "d_prod", 'name': "Дата изготовления" },
            { 'id': "state", 'name': "Статус" },
            { 'id': "node", 'name': "Узел связи" },
            { 'id': "equip", 'name': "Оборудование" },
            { 'id': "d_edit", 'name': "Дата последнего изменения" },
            { 'id': "comment", 'name': "Комментарии", 'sort': False }
            ]


class State(db.Model):
    '''
    Модель таблицы `states` (статус),
    '''

    __tablename__ = 'states'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(50), nullable=False, default='0')
    comment = db.Column(db.String(50))

    accums_rel = db.relationship("Accum", 
                                 back_populates="states_rel", 
                                 uselist=True
                                 )  # связь на уровне моделей MANY accums_rel


    def __repr__(self):
        return f"<Модель 'State': \
            __tablename__ {self.__tablename__}, \
            id {self.id},  \
            state {self.state}, \
            comment {self.comment}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'state': self.state,
            'comment': self.comment
        }
    def get_columns():
        return [
                { 'id': "id", 'name': "id", 'hidden': True },
                { 'id': "state", 'name': "Статус" },
                { 'id': "comment", 'name': "Комментарии", 'sort': False }
                ]


class ModelAccum(db.Model):
    '''
    Модель таблицы `models` (модели аккумулятора),
    '''

    __tablename__ = 'models'
    
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50), comment='Модель аккумулятора')
    manuf = db.Column(db.String(50), comment='Производитель') 
    charge = db.Column(db.Integer, comment='Емкость аккумулятора')
    comment = db.Column(db.String(50))
    accums_rel = db.relationship('Accum', 
                                 back_populates = 'model_rel', 
                                 uselist=True
                                 )  # связь на уровне моделей MANY accums_rel

    def __repr__(self):
        return f"<Модель 'ModelAccum': \
            __tablename__ {self.__tablename__}, \
            id={self.id}, \
            model={self.model}, \
            manuf={self.manuf}, \
            charge={self.charge}, \
            comment={self.comment}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'model': self.model,
            'manuf': self.manuf,
            'charge': self.charge,
            'comment': self.comment,
            # 'accums': [accum for accum in self.accums_rel] 
        }
    def get_columns():
        return [
            { 'id': "id", 'name': "id", 'hidden': True },
            { 'id': "model", 'name': "Модель" },
            { 'id': "manuf", 'name': "Производитель" },
            { 'id': "charge", 'name': "Емкость Ah" },
            { 'id': "comment", 'name': "Комментарии", 'sort': False }
            ]



class Equipment(db.Model):
    '''
    Модель таблицы equip (оборудование)
    '''
    __tablename__ = 'equip'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False, default='0')
    comment =db.Column(db.String(50))
    accum_rel = db.relationship('Accum', 
                                back_populates = 'equips_rel', 
                                uselist=True, 
                                )  # связь на уровне моделей много `accum`

    def __repr__(self):
        return f"<Модель 'Equipment': \
                __tablename__ {self.__tablename__}, \
                id {self.id}, \
                type {self.type}, \
                comment {self.comment}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'comment': self.comment
        }
    def get_columns():
        return [
            { 'id': "id", 'name': "id", 'hidden': True },
            { 'id': "type", 'name': "Оборудование" },
            { 'id': "comment", 'name': "Комментарии", 'sort': False }
            ]

class History(db.Model):
    '''
    Модель таблицы `history` 
    '''    
    __tablename__ = 'history'

    id_rec = db.Column(db.Integer, primary_key=True)
    acc_id = db.Column(db.Integer)
    model = db.Column(db.Integer, nullable=False, default=0)
    No = db.Column(db.String(50))
    d_prod = db.Column(db.DateTime, index=True)
    state = db.Column(db.Integer, default=None)
    node = db.Column(db.Integer, nullable=False, default=0)
    equip = db.Column(db.Integer)
    d_edit = db.Column(db.DateTime, index=True)
    comment = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Используем datetime.utcnow для хранения и даты, и времени

    def __repr__(self):
        return f"History(id={self.id}, acc_id={self.acc_id}, model={self.model}, state={self.state}, timestamp={self.timestamp})"

    def __repr__(self):
        return f"<Модель 'History': \
                    __tablename__ {self.__tablename__}, \
                    id_rec {self.id_rec}, \
                    acc_id {self.acc_id}, \
                    model {self.model}, \
                    No {self.No}, \
                    d_prod {self.d_prod}, \
                    state {self.state},\
                    node {self.node}, \
                    equip {self.equip}, \
                    d_edit {self.d_edit}, \
                    comment {self.comment}, \
                    timestamp={self.timestamp} \
                >"

    def to_dict(self):
        return {
            'id_rec': self.id_rec,
            'acc_id': self.acc_id,
            'model': self.model,
            'No': self.No,
            'd_prod': self.d_prod,
            'state': self.state,
            'node': self.node,
            'equip': self.equip,
            'comment': self.comment
        }
    def get_columns():
        return [
            { 'id': "id", 'name': "id", 'hidden': True },
            { 'id': "acc_id", 'name': "acc_id", 'hidden': True },
            { 'id': "model", 'name': "модель", 'sort': True },
            { 'id': "No", 'name': "No", 'sort': True },
            { 'id': "d_prod", 'name': "d_prod", 'sort': True },
            { 'id': "state", 'name': "Статус", 'sort': True },
            { 'id': "node", 'name': "Узел доступа", 'sort': True },
            { 'id': "equip", 'name': "Оборудование", 'sort': True },
            { 'id': "comment", 'name': "Комментарии", 'sort': True },
            ]
    

class LogCity(db.Model):
    '''Модель таблицы `log_cities` 
    '''
    __tablename__ = 'log_cities'

    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer)
    log_city = db.Column(db.String(50))
    log_comment = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_action = db.Column(db.Integer, db.ForeignKey('users_action.id'))
    user = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __repr__(self):
        return f"<Лог БД 'LogCity': \
            __tablename__ {self.__tablename__}, \
            id {self.id}, \
            log_id {self.log_id}, \
            log_city {self.log_city}, \
            log_comment {self.log_comment}, \
            user {self.user}, \
            user_action {self.user_action}, \
            timestamp {self.timestamp} \
            >"


    def to_dict(self):
        return {
            'id': self.id,
            'log_id': self.log_id,
            'log_city': self.log_city,
            'log_comment': self.log_comment,
            'user': User.query.get(self.user).username if self.user else None,
            'user_action': self.users_action.action,
            'timestamp': self.timestamp
        }

    def get_columns():
      return [
            { 'id': "id", 'name': "id", 'hidden': True },
            { 'id': "log_id", 'name': "city_id ", 'sort': True },
            { 'id': "log_city", 'name': "Города ", 'sort': True },
            { 'id': "log_comment", 'name': "Комментарии ", 'sort': True },
            {'id': "user", 'name': "Пользователь", 'sort': True },
            { 'id': "user_action", 'name': "Действие", 'sort': True },
            { 'id': "timestamp", 'name': "Дата и время изменений ", 'sort': True }
  
              ]



class UserAction(db.Model):
    '''Модель таблицы `users_action` '''
    __tablename__ = 'users_action'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(20), nullable=False, default='0')
    log_city_rel = db.relationship("LogCity", backref="users_action")

    def __repr__(self):
        return f"<Модель 'UserAction': \
            __tablename__ {self.__tablename__}, \
            id {self.id},  \
            action {self.action}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action
        }
    def get_columns():
        return [
                { 'id': "id", 'name': "id", 'hidden': True },
                { 'id': "action", 'name': "Действие" },
                ]


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    '''Модель таблицы `users_action` '''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    log_city_rel = db.relationship("LogCity", backref="users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return f"<Модель 'User': \
            __tablename__ {self.__tablename__}, \
            id {self.id},  \
            username {self.username}, \
            email {self.email}, \
            password_hash {self.password_hash}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email, 
            'password_hash': self.password_hash
        }
    def get_columns():
        return [
                { 'id': "id", 'name': "id", 'hidden': True },
                { 'id': "username", 'name': "Пользователь" },
                { 'id': "email", 'name': "Email" },
                { 'id': "password_hash", 'name': "Пароль" }
                ]