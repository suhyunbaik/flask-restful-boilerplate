from os import environ


class BaseConfig:
    ENV = 'local'
    DEBUG = True
    ECHO_FLAG = True
    READ_DB_URI = environ.get('READ_DB_URI', 'mysql://root@localhost:3306/test')
    WRITE_DB_URI = environ.get('WRITE_DB_URI', 'mysql://root@localhost:3306/test')


class ProductionConfig(BaseConfig):
    ENV = 'develop'


class TestConfig(BaseConfig):
    """
    unittest
    """
    ENV = 'test'
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    READ_DB_URI = ''
    WRITE_DB_URI = ''

