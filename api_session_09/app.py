from flask import Flask, jsonify, request, abort
from blueprints.v1 import bp as v1_bp
from blueprints.v2 import bp as v2_bp
from functools import wraps
LATEST = "2"
SUPPORTED = {"1", "2", "2024-06-20"}
USERS = {1: {"f": "Văn", "l": "Nguyễn", "e": "a@vnu.vn"}}
app = Flask(__name__)
app.register_blueprint(v1_bp, url_prefix="/api/v1/users")
app.register_blueprint(v2_bp, url_prefix="/api/v2/users")
def api_version(supported=SUPPORTED, default=LATEST):
    def decorate(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            v = request.headers.get("X-API-Version", default)
            if v not in supported:
                return jsonify(error="unsupported version"), 400
            result = fn(v, *args, **kwargs)
            response = jsonify(result)
            response.headers["X-API-Version-Served"] = v
            return response
        return wrapper
    return decorate
@app.route("/users/<int:uid>")
@api_version()
def get_user(version, uid):
    u = USERS.get(uid)
    if not u: 
        abort(404, description="user not found")
    if version == "1":
        return {"id": uid, "full_name": u["f"] + " " + u["l"]}
    return {"id": uid, "first_name": u["f"],
    "last_name": u["l"], "email": u["e"]}
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True )
