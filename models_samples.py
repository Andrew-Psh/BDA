# app/models.py

from app import db

class User(db.Model):
    ''' Реализованы связи моделей типа ONE-TO-ONE, ONE-TO-MANY, MANY-TO-MANY.

    1)  ONE-TO-ONE
            модель "User" имеет связь с моделью "House". 
                со стороны "User":
                    house = db.relationship("House", back_populates="user", uselist=False)  # один house
                со стороны "House":
                    user = db.relationship("User", back_populates="house", uselist=False )  # один user

    2)  ONE-TO-MANY
            модель "User" имеет связь с моделью "Address".
                со стороны "User":
                    addresses = db.relationship('Address', back_populates="user", uselist=True)  # много addresses
                со стороны "Address":
                    user = db.relationship('User', back_populates="addresses", uselist=False)  # один user

    3)  MANY-TO-MANY 
            модель "User" имеет связь с моделью "Color" с помощью вспомогательной таблицы user_color.
                со стороны "User":
                    colors = db.relationship("Color", back_populates="user", uselist=True, secondary="user_color")  # много color 
                со стороны "Color":
                    users = db.relationship('User', back_populates="colors", uselist=True, secondary="user_color")  # много users 
    '''
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30))
    addresses = db.relationship('Address', back_populates="user", uselist=True)  # много addresses
    house = db.relationship("House", back_populates="user", uselist=False)    # один house
    colors = db.relationship("Color", back_populates="users", uselist=True, secondary="user_color")    # много colors 


    def __repr__(self) -> str:
        return f"User(id={self.id!r}, firstname={self.firstname!r}, lastname={self.lastname!r})"


class House(db.Model):
    '''
    ONE-TO-ONE 
        модель "House" имеет связь с моделью "User"
            со стороны "House":
                user = db.relationship("User", back_populates="house", uselist=False )  # один user
            со стороны "User":
                house = db.relationship("House", back_populates="user", uselist=False)  # один house
    '''
    __tablename__ = "houses"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    user = db.relationship("User", back_populates="house", uselist=False )   # один user
    user_fk = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"House(id={self.id!r}, name={self.name!r} user_fk={self.user_fk!r})"
    

class Address(db.Model):
    '''
    MANY-TO-ONE 
        модель "Address" имеет связь с моделью "User"
            со стороны "Address":
                user = db.relationship('User', back_populates="addresses", uselist=False)  # один user
            со стороны "User":
                addresses = db.relationship('Address', back_populates="user", uselist=True)  # много addresses
    '''
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(30), unique=True, nullable=False)
    user = db.relationship('User', back_populates="addresses", uselist=False)  # один user
    user_fk = db.Column(db.Integer, db.ForeignKey("users.id")) 

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r}, user_fk={self.user_fk!r})"


class Color(db.Model):
    '''
    MANY-TO-MANY 
        модель "Color" имеет связь с моделью "User" с помощью вспомогательной таблицы user_color.
            со стороны "Color":
                users = db.relationship('User', back_populates="colors", uselist=True, secondary="user_color")  # много users 
            со стороны "User":
                colors = db.relationship("Color", back_populates="users", uselist=True, secondary="user_color")  # много color 
    '''
    __tablename__ = "colors"
    id = db.Column(db.Integer, primary_key=True)
    color_name = db.Column(db.String(30), unique=True, nullable=False)
    users = db.relationship('User', back_populates="colors", uselist=True, secondary="user_color")  # "много users"

    def __repr__(self) -> str:
        return f"Address(id={self.id!r},  color={self.color_name!r})"


class UserColor(db.Model):
    '''
    MANY-TO-MANY 
        модель "UserColor" отражает вспомогательную таблицу user_color, для связи моделей двух таблиц в каждой модели в relationship
        указать вспомогательную таблицу secondary="user_collor" 
            со стороны "Color":
                users = db.relationship('User', back_populates="colors", uselist=True, secondary="user_color")  # много users 
            со стороны "User":
                colors = db.relationship("Color", back_populates="users", uselist=True, secondary="user_color")  # много color 
    '''     
    __tablename__ = "user_color"
    id = db.Column(db.Integer, primary_key=True)
    user_fk = db.Column(db.Integer, db.ForeignKey("users.id")) 
    color_fk = db.Column(db.Integer, db.ForeignKey("colors.id")) 


    
# class User(db.Model):
#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(30))
#     lastname = db.Column(db.String(30))
#     address = db.relationship('Address', backref="user")  # "один"
#     house = db.relationship("House", backref="name", )

#     def __repr__(self) -> str:
#         return f"User(id={self.id}, firstname={self.firstname}, lastname={self.lastname})"


# class House(db.Model):
#     __tablename__ = "houses"
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30))
#     user = db.relationship("User", backref="house", uselist=False )
#     user_fk = db.Column(db.Integer, db.ForeignKey("users.id"))

#     def __repr__(self) -> str:
#         return f"House(id={self.id}, name={self.name} user_fk={self.user_fk})"
    

# class Address(db.Model):
#     # pass
#     __tablename__ = "addresses"
#     id = db.Column(db.Integer, primary_key=True)
#     email_address = db.Column(db.String(30))
#     user = db.relationship('User', backref="address", uselist=False)
#     user_fk = db.Column(db.Integer, db.ForeignKey("users.id"))  # "много"

#     def __repr__(self) -> str:
#         return f"Address(id={self.id},  email_address={self.email_address} user_fk={self.user_fk})"
    

# _________________________________________________________________________________________________
# Фрагмент кода - попытка подключить новый интерфейс SQLalchemy 3.1
# from sqlalchemy.orm import Mapped, mapped_column
# from app import db
# from typing import List
# from typing import Optional

# class User(db.Model):
#     id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
#     username: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
#     email: Mapped[str] = mapped_column(db.String)


# class User(db.Model):
#     __tablename__ = "user"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(db.String(30))
#     fullname: Mapped[Optional[str]]
#     addresses: Mapped[List["Address"]] = db.relationship(back_populates="user")
#     def __repr__(self) -> str:
#         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# class Address(db.Model):
#     __tablename__ = "address"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id = mapped_column(db.ForeignKey("user_account.id"))
#     user: Mapped[User] = db.relationship(back_populates="adresses")
#     def __repr__(self) -> str:
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"

#  Конец фрагмента кода с интерфейсом SQLalchemy 3.1
# _________________________________________________________________________________________________


# _________________________________________________________________________________________________

# Вариант кода по Мега-Учебнику Flask от Miguel Grinberg
# https://habr.com/ru/articles/346344/

# from app import db

# class User(db.Model):
#     __tablename__ = "user"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30))
#     fullname = db.Column(db.String(30))

#     def __repr__(self) -> str:
#         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# class Address(db.Model):
#     __tablename__ = "address"
#     id = db.Column(db.Integer, primary_key=True)
#     email_address = db.Column(db.String(30))

#     def __repr__(self) -> str:
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    
#  Конец кода по Мега-Учебнику Flask
# _________________________________________________________________________________________________
   

# _________________________________________________________________________________________________
# saved

'''# class User(db.Model):
#     __tablename__ = "user"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(db.String(30))
#     fullname: Mapped[Optional[str]]
#     addresses: Mapped[List["Address"]] = db.relationship(back_populates="user")
#     def __repr__(self) -> str:
#         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# class Address(db.Model):
#     __tablename__ = "address"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email_address: Mapped[str]
#     user_id = mapped_column(db.ForeignKey("user_account.id"))
#     user: Mapped[User] = db.relationship(back_populates="adresses")
#     def __repr__(self) -> str:
#         return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    '''