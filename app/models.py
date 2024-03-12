# app/models.py

from app import db

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
                                lazy='dynamic'
                                )  # связь на уровне моделей ONE model
    node_rel = db.relationship('Node', 
                               back_populates = 'accums_rel', 
                               cascade="save-update", 
                               uselist=False, 
                               lazy='dynamic'
                               )  # связь на уровне моделей ONE node

    states_rel = db.relationship("State", 
                                back_populates="accums_rel", 
                                cascade="save-update", 
                                uselist=False, 
                                # lazy='dynamic'
                                ) 

    equips_rel = db.relationship('Equipment', 
                                 back_populates="accum_rel", 
                                 cascade="save-update", 
                                 uselist=True, 
                                 lazy='dynamic'
                                 )  # связь на уровне моделей MANY equips_rel

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
            'model': self.model, 
            'No': self.No, 
            'd_prod': self.d_prod, 
            'state': self.state, 
            'node': self.node, 
            'equip': self.equip, 
            'd_edit': self.d_edit, 
            'comment': self.comment
        }



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
        return f"<Модель 'Node': \
            __tablename__ {self.__tablename__}, \
            id {self.id}, addr {self.addr}, \
            city {self.city}, street {self.street}, \
            house {self.house}, place {self.place}, \
            comment {self.comment}>"
  
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


class Equipment(db.Model):
    '''
    Модель таблицы equip (оборудование)
    '''
    __tablename__ = 'equip'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False, default='0')
    comment =db.Column(db.String(50))
    accum_rel = db.relationship('Accums', 
                                back_populates = 'equip_rel', 
                                uselist=False, 
                                )  # связь на уровне моделей один `accum`

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
                    timestamp={self.timestamp}>"

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
                                lazy='dynamic'
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


 




   







##########################    BEGINNING TEMPLATES       #####################################
    
# промежуточная таблица 'characters_colors' для связи многие ко многим в таблицах 'characters' и 'colors'
characters_colors = db.Table('characters_colors',
    db.Column('character_id', db.Integer, db.ForeignKey('characters.id'), primary_key=True),
    db.Column('color_id', db.Integer, db.ForeignKey('colors.id'), primary_key=True)
)

class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    addresses = db.relationship('Address', backref='owner', lazy='dynamic')
    colors = db.relationship('Color', secondary=characters_colors, backref='characters', lazy='dynamic')

class Color(db.Model):
    __tablename__ = 'colors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class Address(db.Model):
    __tablename__ = 'addresses'  # Наименование таблицы для адресов

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

##########################          END TEMPLATES       #####################################
