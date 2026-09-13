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


# Bai 4
# from flask import Flask, jsonify, request
# app = Flask(__name__)
# BOOKS = [
#     {"id": "z2a3b4", "title": "bro jump", "price": 150, "item_id" : 20},
#     {"id": "1a2b3c", "title": "trust me bro", "price": 200, "item_id" : 1},
#     {"id": "c2b31a", "title": "atomic bro", "price": 300, "item_id" : 2},
#     {"id": "cccmmb", "title": "Top 100 anime op", "price": 100, "item_id" : 3},
#     {"id": "d4e5f6", "title": "Pygame Mastery", "price": 250, "item_id" : 4},
#     {"id": "g7h8i9", "title": "Tử Vi Đẩu Số Toàn Thư", "price": 450, "item_id" : 5},
#     {"id": "j0k1l2", "title": "IELTS Writing Task 2", "price": 150, "item_id" : 6},
#     {"id": "m3n4o5", "title": "Hiragana for Beginners", "price": 120, "item_id" : 7},
#     {"id": "p6q7r8", "title": "MIPS & Java Fundamentals", "price": 350, "item_id" : 8},
#     {"id": "s9t0u1", "title": "Flask API Design not for this bro", "price": 280, "item_id" : 9},
#     {"id": "v2w3x4", "title": "The Tarot Guide", "price": 180, "item_id" : 10},
#     {"id": "y5z6a7", "title": "Leg Day: The Hack Squat", "price": 110, "item_id" : 11},
#     {"id": "b8c9d0", "title": "IEM Acoustic Signatures", "price": 400, "item_id" : 12},
#     {"id": "e1f2g3", "title": "RimWorld Modding 101", "price": 220, "item_id" : 13},
#     {"id": "h4i5j6", "title": "Relational Schemas Explained", "price": 310, "item_id" : 14},
#     {"id": "k7l8m9", "title": "A* and Beyond: AI Search", "price": 380, "item_id" : 15},
#     {"id": "n0o1p2", "title": "Clean Architecture in Python", "price": 420, "item_id" : 16},
#     {"id": "q3r4s5", "title": "Kinh Dịch Lược Giải", "price": 260, "item_id" : 17},
#     {"id": "t6u7v8", "title": "Software Design Patterns for bro", "price": 330, "item_id" : 18},
#     {"id": "w9x0y1", "title": "Dijkstra's Path", "price": 190, "item_id" : 19},
    
# ]

# def find_by_id(book_id):
#     for book in BOOKS:
#         if book["id"] == book_id:
#             return book
#     return None

# def finditem_by_id(item_id):
#     for book in BOOKS:
#         if book["item_id"] == item_id:
#             return book
#     return None
# #path params
# @app.route("/books/<book_id>", methods = ["GET"])
# def get_book(book_id):
#     book = find_by_id(book_id)
#     if book is None:
#         return jsonify({"error" : "not found"}), 404
#     return jsonify(book), 200
# @app.route("/items/<int:item_id>")
# def get_item(item_id):
#     item = finditem_by_id(item_id)
#     if item is None:
#         return jsonify({"error" : "not found"}), 404
#     return jsonify({"id":item_id}), 200
    


# #query string
# @app.route("/books", methods=["GET"])
# def list_books():
#     limit = int(request.args.get("limit", 20))
#     q = request.args.get("q","").strip().lower()
#     sort = request.args.get("s", "").strip().lower()
#     items = [b for b in BOOKS if q in b["title"].lower()]
#     if sort == "item_id":
#         items = sorted(items, key=lambda x: x["item_id"])
#     elif sort== "-item_id":
#         items = sorted(items, key=lambda x: x["item_id"], reverse=True)
#     items = items[:limit]
#     return jsonify({"items": items}), 200
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True)

from flask import Flask,jsonify
ORDERS = {
    "ORD001": {"guest_name": "Nguyen Van A", "status": "pending", "time": "2026-09-14 08:00", "money": 150000},
    "ORD002": {"guest_name": "Tran Thi B", "status": "shipped", "time": "2026-09-13 14:30", "money": 250000},
    "ORD003": {"guest_name": "Le Van C", "status": "delivered", "time": "2026-09-12 10:15", "money": 320000},
    "ORD004": {"guest_name": "Pham Thi D", "status": "processing", "time": "2026-09-14 09:45", "money": 120000},
    "ORD005": {"guest_name": "Hoang Van E", "status": "pending", "time": "2026-09-14 11:20", "money": 450000},
    "ORD006": {"guest_name": "Vu Thi F", "status": "shipped", "time": "2026-09-13 09:00", "money": 50000},
    "ORD007": {"guest_name": "Ngo Van G", "status": "delivered", "time": "2026-09-11 16:20", "money": 780000},
    "ORD008": {"guest_name": "Do Thi H", "status": "pending", "time": "2026-09-14 12:00", "money": 210000},
    "ORD009": {"guest_name": "Bui Van I", "status": "processing", "time": "2026-09-14 07:10", "money": 340000},
    "ORD010": {"guest_name": "Dang Thi K", "status": "shipped", "time": "2026-09-13 10:30", "money": 890000},
    "ORD011": {"guest_name": "Ton Van L", "status": "pending", "time": "2026-09-14 12:30", "money": 115000},
    "ORD012": {"guest_name": "Phan Thi M", "status": "delivered", "time": "2026-09-09 14:00", "money": 400000},
    "ORD013": {"guest_name": "Ly Van N", "status": "processing", "time": "2026-09-14 09:45", "money": 280000},
    "ORD014": {"guest_name": "Dao Thi O", "status": "shipped", "time": "2026-09-12 11:15", "money": 600000},
    "ORD015": {"guest_name": "Truong Van P", "status": "pending", "time": "2026-09-14 12:40", "money": 225000},
    "ORD016": {"guest_name": "Trinh Thi Q", "status": "delivered", "time": "2026-09-08 08:00", "money": 150000},
    "ORD017": {"guest_name": "Mai Van R", "status": "processing", "time": "2026-09-14 10:05", "money": 199000},
    "ORD018": {"guest_name": "Dinh Thi S", "status": "shipped", "time": "2026-09-13 16:50", "money": 275000},
    "ORD019": {"guest_name": "Phung Van T", "status": "pending", "time": "2026-09-14 12:45", "money": 310000},
    "ORD020": {"guest_name": "Chau Thi U", "status": "delivered", "time": "2026-09-07 19:30", "money": 550000}
}
app = Flask(__name__)
@app.route("/orders/<order_id>", methods = ["DELETE"])
def delete_order(order_id):
    order = ORDERS.get(order_id)
    if order is None:
        return {"error" : "Not Found"}, 404
    if order["status"] in ("shipped", "delivered"):
        return {"error": "Cannot Delete"}, 409
    ORDERS.pop(order_id, None)
    return "", 204
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)