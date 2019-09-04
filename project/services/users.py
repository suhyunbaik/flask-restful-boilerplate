from project.databases import read_session, write_session
from marshmallow import Schema, fields
from project.models.user import User


class UserSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)


class UserController:
    def __init__(self, session):
        self._session = read_session if session == 'read' else write_session

    def get_users(self):
        return self._session.query(User).all()




