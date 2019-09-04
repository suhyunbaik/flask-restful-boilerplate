import os
import pytest
import json
from sqlalchemy.orm import sessionmaker
from project.app import create_app
from project.databases import Base
from project.models.user import User


@pytest.fixture(scope='session')
def app():
    os.environ['SERVICE_ENV'] = 'config.TestConfig'
    app = create_app()
    app_context = app.app_context()
    app_context.push()
    yield app
    app_context.pop()


@pytest.fixture(scope='session')
def init_db(app):
    engine = app.db._generate_engine(app.config['WRITE_DB_URI'])
    meta = Base.metadata
    meta.bind = engine
    meta.create_all()
    yield engine
    meta.drop_all()
    engine.dispose()


@pytest.fixture(scope='session')
def client(app, init_db):
    return app.test_client()


@pytest.fixture(scope='module')
def session(init_db):
    Session = sessionmaker(bind=init_db)
    session = Session()
    yield session
    session.rollback()
    session.close_all()


def read_data_set(fname):
    with open('{}/tests/fixture/dataset/{}.json'.format(os.path.dirname(os.path.realpath(__file__)), fname), 'r') as file:
        return json.load(file)


def read_input_set(fname):
    with open('{}/tests/fixture/inputcase/{}.json'.format(os.path.dirname(os.path.realpath(__file__)), fname), 'r') as file:
        return json.load(file)


def read_output_set(fname):
    with open('{}/tests/fixture/outputcase/{}.json'.format(os.path.dirname(os.path.realpath(__file__)), fname), 'r') as file:
        return json.load(file)


@pytest.fixture(scope='function')
def active_user(session):
    data = read_data_set('active_user')
    user = User(id=data['user']['id'], name=data['user']['name'])
    session.add(user)
    session.commit()
    yield
    session.query(User).delete()
    session.commit()


