
from flask import Blueprint, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from extensions import db

health_bp = Blueprint("health", __name__)


@health_bp.get("/healthz")
def healthz():
    return jsonify({"status": "ok"}), 200


@health_bp.get("/ready")
def ready():
    try:
        db.session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({
            "status": "degraded",
            "checks": {"db": "err"}
        }), 503

    return jsonify({
        "status": "ok",
        "checks": {"db": "ok"}
    }), 200
