from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


# Модель пользователей
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.Integer(100), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    phones = db.relationship('Phone', back_populates = 'user', cascade='all, delete-orphan')


    def __repr__(self):
        return f"<User {self.id} {self.name}>"\
        

# Можель телефонов
class Phone(db.Model):
    __tablename__ = 'phones'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', nullable=False))

    user = db.relationship("User", back_populates = 'phones')


    def __repr__(self):
        return f'<Phone {self.id} {self.phone_number} for user {self.user_id}'
    
