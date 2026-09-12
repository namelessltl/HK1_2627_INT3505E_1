# #Bai 1
# from flask import Flask
# app = Flask(__name__)
# @app.route("/")
# def index():
#     return "Hello World"
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True)


# Bai 2
from flask import Flask,jsonify,request
app = Flask(__name__)
# GET /health — kiểm tra server còn sống
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Circle K"}), 200
# POST /chocolate — trả lại cái client gửi
@app.route("/chocolate", methods=["POST"])
def chocolate():
    data = request.get_json(silent=True) or {}
    return jsonify({"you_sent": data}), 200
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)