import functools
import logging
import os
import threading
from typing import Any, Optional

import jwt
from flask import Flask, jsonify, request
from flask_cors import CORS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(threadName)s: %(message)s",
)
logger = logging.getLogger("students_api")

# Local-development default only. Set JWT_SECRET in the environment in production.
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-only-secret-change-this-before-deploying-2026")


class StudentDatastore:
    """Thread-safe in-memory datastore for students."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._students: dict[int, dict[str, Any]] = {
            1: {"id": 1, "name": "Nguyễn Văn An", "className": "K69"},
            2: {"id": 2, "name": "Trần Thị Bình", "className": "K69"},
            3: {"id": 3, "name": "Lê Minh Cường", "className": "K70"},
        }
        self._next_id = 4

    def list_students(
        self, limit: int = 20, class_name: Optional[str] = None
    ) -> list[dict[str, Any]]:
        with self._lock:
            students = list(self._students.values())
            if class_name is not None:
                students = [s for s in students if s["className"] == class_name]
            return [student.copy() for student in students[:limit]]

    def get_student(self, student_id: int) -> Optional[dict[str, Any]]:
        with self._lock:
            student = self._students.get(student_id)
            return student.copy() if student is not None else None

    def create_student(self, name: str, class_name: str) -> dict[str, Any]:
        with self._lock:
            student_id = self._next_id
            self._next_id += 1
            student = {
                "id": student_id,
                "name": name,
                "className": class_name,
            }
            self._students[student_id] = student
            return student.copy()

    def update_student(
        self, student_id: int, updates: dict[str, str]
    ) -> Optional[dict[str, Any]]:
        with self._lock:
            student = self._students.get(student_id)
            if student is None:
                return None
            student.update(updates)
            return student.copy()

    def delete_student(self, student_id: int) -> bool:
        with self._lock:
            return self._students.pop(student_id, None) is not None


datastore = StudentDatastore()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JWT_SECRET"] = JWT_SECRET
    CORS(app, allow_headers=["Content-Type", "Authorization"])

    def error(message: str, status: int):
        return jsonify({"message": message}), status

    def require_bearer_token(func):
        @functools.wraps(func)
        def decorated_function(*args, **kwargs):
            authorization = request.headers.get("Authorization", "")
            parts = authorization.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                return error("Thiếu token hoặc token không hợp lệ", 401)

            try:
                jwt.decode(
                    parts[1],
                    app.config["JWT_SECRET"],
                    algorithms=["HS256"],
                )
            except jwt.PyJWTError:
                return error("Thiếu token hoặc token không hợp lệ", 401)

            return func(*args, **kwargs)

        return decorated_function

    def parse_student_id(raw_id: str) -> Optional[int]:
        if not raw_id.isascii() or not raw_id.isdecimal():
            return None
        student_id = int(raw_id)
        return student_id if student_id >= 1 else None

    def validate_student_payload(data: Any, create: bool) -> Optional[str]:
        if not isinstance(data, dict):
            return "Body phải là một JSON object"
        if not data:
            return "Phải cung cấp ít nhất một trường để cập nhật"

        allowed_fields = {"name", "className"}
        if set(data) - allowed_fields:
            return "Body chỉ được chứa các trường 'name' và 'className'"
        if create and not allowed_fields.issubset(data):
            return "Cần cung cấp cả 'name' và 'className'"
        for field, value in data.items():
            if not isinstance(value, str) or len(value) < 1:
                return f"Trường '{field}' phải là chuỗi có ít nhất 1 ký tự"
        return None

    @app.errorhandler(400)
    def handle_bad_request(err):
        return error("Yêu cầu không hợp lệ", 400)

    @app.errorhandler(401)
    def handle_unauthorized(err):
        return error("Thiếu token hoặc token không hợp lệ", 401)

    @app.errorhandler(404)
    def handle_not_found(err):
        return error("Không tìm thấy tài nguyên", 404)

    @app.errorhandler(405)
    def handle_method_not_allowed(err):
        return error("Phương thức HTTP không được hỗ trợ", 405)

    @app.errorhandler(422)
    def handle_validation_error(err):
        return error("Tham số hoặc dữ liệu gửi lên không hợp lệ", 422)

    @app.errorhandler(500)
    def handle_internal_server_error(err):
        logger.exception("Internal server error")
        return error("Lỗi máy chủ nội bộ", 500)

    @app.route("/v1/students", methods=["GET"])
    @require_bearer_token
    def list_students():
        raw_limit = request.args.get("limit", "20")
        if not raw_limit.isascii() or not raw_limit.isdecimal():
            return error("'limit' phải là số nguyên từ 1 đến 100", 422)
        limit = int(raw_limit)
        if not 1 <= limit <= 100:
            return error("'limit' phải là số nguyên từ 1 đến 100", 422)

        class_name = request.args.get("className")
        students = datastore.list_students(limit=limit, class_name=class_name)
        return jsonify(students), 200

    @app.route("/v1/students", methods=["POST"])
    @require_bearer_token
    def create_student():
        if not request.is_json:
            return error("Body phải có Content-Type: application/json", 422)

        data = request.get_json(silent=True)
        message = validate_student_payload(data, create=True)
        if message is not None:
            return error(message, 422)

        created = datastore.create_student(data["name"], data["className"])
        return jsonify(created), 201

    @app.route("/v1/students/<student_id>", methods=["GET"])
    @require_bearer_token
    def get_student(student_id: str):
        parsed_id = parse_student_id(student_id)
        if parsed_id is None:
            return error("'id' phải là số nguyên lớn hơn hoặc bằng 1", 422)

        student = datastore.get_student(parsed_id)
        if student is None:
            return error("Không tìm thấy sinh viên có ID này", 404)
        return jsonify(student), 200

    @app.route("/v1/students/<student_id>", methods=["PATCH"])
    @require_bearer_token
    def update_student(student_id: str):
        parsed_id = parse_student_id(student_id)
        if parsed_id is None:
            return error("'id' phải là số nguyên lớn hơn hoặc bằng 1", 422)
        if datastore.get_student(parsed_id) is None:
            return error("Không tìm thấy sinh viên có ID này", 404)
        if not request.is_json:
            return error("Body phải có Content-Type: application/json", 422)

        data = request.get_json(silent=True)
        message = validate_student_payload(data, create=False)
        if message is not None:
            return error(message, 422)

        updated = datastore.update_student(parsed_id, data)
        if updated is None:
            return error("Không tìm thấy sinh viên có ID này", 404)
        return jsonify(updated), 200

    @app.route("/v1/students/<student_id>", methods=["DELETE"])
    @require_bearer_token
    def delete_student(student_id: str):
        parsed_id = parse_student_id(student_id)
        if parsed_id is None:
            return error("'id' phải là số nguyên lớn hơn hoặc bằng 1", 422)

        if not datastore.delete_student(parsed_id):
            return error("Không tìm thấy sinh viên có ID này", 404)
        return "", 204

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
