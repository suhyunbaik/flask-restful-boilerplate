from flask import jsonify
from flask_restful import Resource

from project.services.users import UserController, UserSchema


class Users(Resource):
    def get(self):
        """
        유저 상세정보
        ---
        responses:
          200:
            description: 유저 상세정보
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: 유저 pk
                name:
                  type: string
                  description: 유저 이름
        """
        user = UserController('read').get_users()
        if not user:
            return jsonify(users=[])

        users = UserSchema().dump(user)
        return jsonify(users=users)

