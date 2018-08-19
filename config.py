class Config(object):
    DEBUG = True
    Testing = False
    DATABASE_NAME = "papers"

class DevelopmentConfig(Config):
    SECRET_KEY = "S9893JKJSkdfu9"

config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': DevelopmentConfig
}