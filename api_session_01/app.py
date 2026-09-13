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
# from flask import Flask,jsonify,request
# from uuid import uuid4
# app = Flask(__name__)
# STUDENTS = []
# @app.route("/students", methods= ["POST"])
# def create_students():
#     body = request .get_json(silent=True) or {}
#     name = body.get("name")
#     if not name:
#         return jsonify({"error":"NEED A NAME"}), 400
#     student = {
#         "id": str(uuid4()),
#         "name": name,
#         "gpa": body.get("gpa", 0.0),
#     }
#     STUDENTS.append(student)
#     response = jsonify(student)
#     response.status_code = 201
#     response.headers["Location"] = f"/students/{student['id']}"
#     return response

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True)

from flask import Flask, jsonify, request
app = Flask(__name__)
BOOKS = [
    {"id": "1a2b3c", "title": "trust me bro", "price": 200, "item_id" : 1},
    {"id": "c2b31a", "title": "atomic bro", "price": 300, "item_id" : 2},
    {"id": "cccmmb", "title": "Top 100 anime op", "price": 100, "item_id" : 3},
    {"id": "d4e5f6", "title": "Pygame Mastery", "price": 250, "item_id" : 4},
    {"id": "g7h8i9", "title": "Tử Vi Đẩu Số Toàn Thư", "price": 450, "item_id" : 5},
    {"id": "j0k1l2", "title": "IELTS Writing Task 2", "price": 150, "item_id" : 6},
    {"id": "m3n4o5", "title": "Hiragana for Beginners", "price": 120, "item_id" : 7},
    {"id": "p6q7r8", "title": "MIPS & Java Fundamentals", "price": 350, "item_id" : 8},
    {"id": "s9t0u1", "title": "Flask API Design not for this bro", "price": 280, "item_id" : 9},
    {"id": "v2w3x4", "title": "The Tarot Guide", "price": 180, "item_id" : 10},
    {"id": "y5z6a7", "title": "Leg Day: The Hack Squat", "price": 110, "item_id" : 11},
    {"id": "b8c9d0", "title": "IEM Acoustic Signatures", "price": 400, "item_id" : 12},
    {"id": "e1f2g3", "title": "RimWorld Modding 101", "price": 220, "item_id" : 13},
    {"id": "h4i5j6", "title": "Relational Schemas Explained", "price": 310, "item_id" : 14},
    {"id": "k7l8m9", "title": "A* and Beyond: AI Search", "price": 380, "item_id" : 15},
    {"id": "n0o1p2", "title": "Clean Architecture in Python", "price": 420, "item_id" : 16},
    {"id": "q3r4s5", "title": "Kinh Dịch Lược Giải", "price": 260, "item_id" : 17},
    {"id": "t6u7v8", "title": "Software Design Patterns for bro", "price": 330, "item_id" : 18},
    {"id": "w9x0y1", "title": "Dijkstra's Path", "price": 190, "item_id" : 19},
    {"id": "z2a3b4", "title": "bro jump", "price": 150, "item_id" : 20},
]

def find_by_id(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None

def finditem_by_id(item_id):
    for book in BOOKS:
        if book["item_id"] == item_id:
            return book
    return None
#path params
@app.route("/books/<book_id>", methods = ["GET"])
def get_book(book_id):
    book = find_by_id(book_id)
    if book is None:
        return jsonify({"error" : "not found"}), 404
    return jsonify(book), 200
@app.route("/items/<int:item_id>")
def get_item(item_id):
    item = finditem_by_id(item_id)
    if item is None:
        return jsonify({"error" : "not found"}), 404
    return jsonify({"id":item_id}), 200
    


#query string
@app.route("/books", methods=["GET"])
def list_books():
    limit = int(request.args.get("limit", 20))
    q = request.args.get("q","").strip().lower()
    items = [b for b in BOOKS if q in b["title"].lower()]
    items = items[:limit]
    return jsonify({"items": items}), 200
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)