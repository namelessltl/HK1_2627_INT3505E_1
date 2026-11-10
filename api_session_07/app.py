
import os

from flask import Flask, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from extensions import db, migrate
from api.products import products_bp
from api.orders import orders_bp
from api.health import health_bp

import models


def create_app(config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DB_URL", "sqlite:///dev.db"
    )

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(health_bp)

    @app.errorhandler(ValidationError)
    def validation_error(err):
        return jsonify({
            "error": "validation_error",
            "detail": err.messages
        }), 422

    @app.errorhandler(HTTPException)
    def http_error(err):
        return jsonify({
            "error": err.name.lower().replace(" ", "_"),
            "detail": err.description
        }), err.code

    @app.errorhandler(Exception)
    def server_error(err):
        if app.config.get("TESTING"):
            raise err

        app.logger.exception("unhandled error")
        return jsonify({
            "error": "internal_error",
            "detail": "internal server error"
        }), 500

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
