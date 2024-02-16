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

   
class Color(db.Model):
  
    __tablename__ = 'colors'

    id = db.Column(db.Integer, primary_key=True)
    color_name = db.Column(db.String(50), nullable=False, default='0',  unique=True)

    def __repr__(self):
        return f'<Модель `Color`: __tablename__ {self.__tablename__}, id {self.id}, color_name {self.color_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'color_name': self.color_name
        }

class Address(db.Model):
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50), default='Bikini Bottom',  unique=False)

    def __repr__(self):
        return f'<Модель {self.name}: __tablename__ {self.__tablename__}, id {self.id}, color_name {self.color_name}>'
