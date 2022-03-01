import os
class Config(object):
    SECRET_KEY = 'pc38nm2389c43249m8c234mc123m40nc13294c01329c48nm2384c9un213c48193c4un1239c4m123u4n'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'seidorvet'
    JSON_AS_ASCII = False
    CORS_HEADERS = "Content-Type"
class DevelopmentConfig(Config):
    DEBUG = True