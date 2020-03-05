
import os

class Config(object):
    DEBUG = False
    SECRET_KEY = '123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../src/contenedores.sqlite'
    SQLALCHEMY_BINDS = {
        'Containers': SQLALCHEMY_DATABASE_URI,
        'Users': 'sqlite:///../src/users.db'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    #SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../src/contenedores.sqlite'
    SQLALCHEMY_BINDS = {
        'Containers': SQLALCHEMY_DATABASE_URI,
        'Users': 'sqlite:///../src/users.db'
    }

class DevelopmentConfig(Config):
    DEBUG = True