import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_swagger import swagger
from project.controller.users import Users
from project.databases import DB, db


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.getenv('SERVICE_ENV', 'config.BaseConfig'))
    app.register_blueprint(db)
    DB(app)

    @app.route('/ping')
    def ping():
        return jsonify(ok='ok')

    api = Api(app)
    api.add_resource(Users, '/users')

    if app.config['ENV'] != 'config.ProductionConfig':
        @app.route('/spec')
        def spec():
            swag = swagger(app)
            swag['description'] = 'Flask boilerplate API'
            swag['info']['version'] = '1.0'
            swag['info']['title'] = 'Flask boilerplate API'
            return jsonify(swag)

        @app.route('/urls')
        def urls():
            return jsonify([str(p) for p in app.url_map.iter_rules()])

        import sys
        import logging
        logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.dialects').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
        logging.getLogger('sqlalchemy.orm').setLevel(logging.WARN)
        logging.basicConfig(level=logging.DEBUG,
                            stream=sys.stdout,
                            format='%(asctime)s %(levelname)s %(name)s %(message)s')

    return app
