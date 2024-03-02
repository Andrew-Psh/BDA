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