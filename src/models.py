from sqlalchemy import Boolean, Column , ForeignKey
from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from src.app import db


class Containers(db.Model):
    
    __tablename__ = 'contenedores'
    __bind_key__ = 'Containers'

    GID = Column(String(255), primary_key=True)
    CCZ = Column(String(255))
    COD_IMM = Column(String(255))
    DIRECCION = Column(String(255))
    NOMBRE_CON = Column(String(255))


class Users(db.Model):

    __tablename__ = 'users'
    __bind_key__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
