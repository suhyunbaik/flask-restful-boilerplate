from flask import request, has_request_context, Blueprint, current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.local import LocalProxy


Base = declarative_base()
db = Blueprint('db', __name__)


class DB:
    def __init__(self, app):
        self.app = app
        app.db = self

        self.write_engine = self._generate_engine(app.config['WRITE_DB_URI'])
        self.read_engine = self._generate_engine(app.config['READ_DB_URI'])

        self.write_session = self._generate_session(self.write_engine)
        self.read_session = self._generate_session(self.read_engine)

    def _generate_engine(self, uri):
        return create_engine(
            uri,
            pool_recycle=900,
            pool_size=10,
            max_overflow=15,
            isolation_level='READ_COMMITTED'
        )

    def _generate_session(self, engine):
        return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


class DebugContext:
    pass


debug_context = DebugContext()


@LocalProxy
def read_session():
    if has_request_context():
        ctx = request._get_current_object()
    else:
        ctx = debug_context
    try:
        session_ = ctx._current_read_session
    except AttributeError:
        session_ = current_app.db.read_session()
        ctx._current_read_session = session_
    return session_


@LocalProxy
def write_session():
    if has_request_context():
        ctx = request._get_current_object()
    else:
        ctx = debug_context
    try:
        session_ = ctx._current_write_session
    except AttributeError:
        session_ = current_app.db.write_session()
        ctx._current_write_session = session_
    return session_


@db.teardown_app_request
def close_session(exception=None, *args, **kwargs):
    if has_request_context():
        ctx = request._get_current_object()
    else:
        ctx = args[1]

    if hasattr(ctx, '_current_read_session'):
        if exception is not None:
            ctx._current_read_session.rollback()
        ctx._current_read_session.close()

    if hasattr(ctx, '_current_write_session'):
        if exception is not None:
            ctx._current_write_session.rollback()
        ctx._current_write_session.close()
