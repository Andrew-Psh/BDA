# app/models.py

from app import db


class User(db.Model):

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, default='0', unique=True)
   
    def __repr__(self):
        return f'<Модель `User`: tablename {self.__tablename__}, id {self.id}, name {self.name},>'
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

# Модель для адреса
class Address(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

# Модель для цвета
class Color(db.Model):
    __tablename__ = 'color'

    id = db.Column(db.Integer, primary_key=True)
    color_name = db.Column(db.String)

# Модель для персонажей
class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Связь один ко многим с адресами
    addresses = db.relationship('Address', backref='character', lazy=True)

    # Связь многие ко многим с цветами
    colors = db.relationship('Color', secondary='character_color')

# Связующая таблица для связи многие ко многим между персонажами и цветами
character_color = db.Table('character_color',
                           db.Column('character_id', db.Integer, db.ForeignKey('characters.id')),
                           db.Column('color_id', db.Integer, db.ForeignKey('color.id'))
                           )

##########################          draft       #####################################
# class Color(db.Model):
#     __tablename__ = 'colors'

#     id = db.Column(db.Integer, primary_key=True)
#     color_name = db.Column(db.String, unique=True, nullable=False)
    
#     characters = db.relationship("Сharacter", secondary="characters_colors")

#     def __repr__(self):
#         return f"<Color(color_name='{self.color_name}')>"

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'color_name': self.color_name,
#         }

# class Address(db.Model):
#     __tablename__ = 'addresses'  # Обратите внимание на двойное подчеркивание перед и после 'tablename'

#     id = db.Column(db.Integer, primary_key=True)
#     address = db.Column(db.String(50), default='Bikini Bottom', unique=False)

#     characters = db.relationship("Character", back_populates="address")  # Исправлено на "Character" и "address"

#     def repr(self):  # Поддержка внутреннего метода repr
#         return f'<Address {self.id}: {self.address}>'


# class Character(db.Model):
#     __tablename__ = 'characters'  # Обратите внимание на двойное подчеркивание перед и после 'tablename'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True, nullable=False)

#     address_id = db.Column(db.Integer, db.ForeignKey('addresses.id'))
#     address = db.relationship("Address", back_populates="characters", foreign_keys=[address_id])

#     colors = db.relationship("Color", secondary="characters_colors")

#     def repr(self):
#         return f"<Character(name='{self.name}')>"

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'address_id': self.address_id,
#             'colors': [color.to_dict() for color in self.colors]
#         }
    


# class characters_colors(db.Model):
#     __tablename__ = 'characters_colors'
    
#     character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), primary_key=True)
#     color_id = db.Column(db.Integer, db.ForeignKey('colors.id'), primary_key=True)
##########################       end   draft       #####################################
