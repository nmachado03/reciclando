import os

secret_key = '123'

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///contenedores.sqlite'
SQLALCHEMY_BINDS = {
    'Containers': SQLALCHEMY_DATABASE_URI,
    'Users': 'sqlite:///users.db'
}
SQLALCHEMY_TRACK_MODIFICATIONS = False