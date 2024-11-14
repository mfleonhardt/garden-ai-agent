from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
import logging

from .api.garden_location import garden_location_ns
from .api.irrigation_zone import irrigation_zone_ns
from .api.plant import plant_ns
from .data.database import db


def initialize_api(app):
    # Initialize API
    api = Api(app, version='1.0', title='Garden API',
              description='A simple API for managing garden data')

    # Register namespaces
    api.add_namespace(garden_location_ns)
    api.add_namespace(irrigation_zone_ns)
    api.add_namespace(plant_ns)


def create_app(test_config=None):
    app = Flask(__name__)

    # Default Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garden_data.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Override with test config if provided
    if test_config is not None:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)

    # Logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('werkzeug').setLevel(logging.INFO)

    initialize_api(app)
    return app

