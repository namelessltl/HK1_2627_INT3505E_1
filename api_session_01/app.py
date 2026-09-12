# #Bai 1
# from flask import Flask
# app = Flask(__name__)
# @app.route("/")
# def index():
#     return "Hello World"
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True)


# Bai 2
# from flask import Flask,jsonify,request
# app = Flask(__name__)
# # GET /health — kiểm tra server còn sống
# @app.route("/health", methods=["GET"])
# def health():
#     return jsonify({"status": "Circle K"}), 200
# # POST /chocolate — trả lại cái client gửi
# @app.route("/chocolate", methods=["POST"])
# def chocolate():
#     data = request.get_json(silent=True) or {}
#     return jsonify({"you_sent": data}), 200
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True)

# bai 3
from flask import Flask,jsonify,request
from uuid import uuid4
app = Flask(__name__)
STUDENTS = []
@app.route("/students", methods= ["POST"])
def create_students():
    body = request .get_json(silent=True) or {}
    name = body.get("name")
    if not name:
        return jsonify({"error":"NEED A NAME"}), 400
    student = {
        "id": str(uuid4()),
        "name": name,
        "gpa": body.get("gpa", 0.0),
    }
    STUDENTS.append(student)
    response = jsonify(student)
    response.status_code = 201
    response.headers["Location"] = f"/students/{student['id']}"
    return response

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)