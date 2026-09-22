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

# from flask import Flask,jsonify
# ORDERS = {
#     "ORD001": {"guest_name": "Nguyen Van A", "status": "pending", "time": "2026-09-14 08:00", "money": 150000},
#     "ORD002": {"guest_name": "Tran Thi B", "status": "shipped", "time": "2026-09-13 14:30", "money": 250000},
#     "ORD003": {"guest_name": "Le Van C", "status": "delivered", "time": "2026-09-12 10:15", "money": 320000},
#     "ORD004": {"guest_name": "Pham Thi D", "status": "processing", "time": "2026-09-14 09:45", "money": 120000},
#     "ORD005": {"guest_name": "Hoang Van E", "status": "pending", "time": "2026-09-14 11:20", "money": 450000},
#     "ORD006": {"guest_name": "Vu Thi F", "status": "shipped", "time": "2026-09-13 09:00", "money": 50000},
#     "ORD007": {"guest_name": "Ngo Van G", "status": "delivered", "time": "2026-09-11 16:20", "money": 780000},
#     "ORD008": {"guest_name": "Do Thi H", "status": "pending", "time": "2026-09-14 12:00", "money": 210000},
#     "ORD009": {"guest_name": "Bui Van I", "status": "processing", "time": "2026-09-14 07:10", "money": 340000},
#     "ORD010": {"guest_name": "Dang Thi K", "status": "shipped", "time": "2026-09-13 10:30", "money": 890000},
#     "ORD011": {"guest_name": "Ton Van L", "status": "pending", "time": "2026-09-14 12:30", "money": 115000},
#     "ORD012": {"guest_name": "Phan Thi M", "status": "delivered", "time": "2026-09-09 14:00", "money": 400000},
#     "ORD013": {"guest_name": "Ly Van N", "status": "processing", "time": "2026-09-14 09:45", "money": 280000},
#     "ORD014": {"guest_name": "Dao Thi O", "status": "shipped", "time": "2026-09-12 11:15", "money": 600000},
#     "ORD015": {"guest_name": "Truong Van P", "status": "pending", "time": "2026-09-14 12:40", "money": 225000},
#     "ORD016": {"guest_name": "Trinh Thi Q", "status": "delivered", "time": "2026-09-08 08:00", "money": 150000},
#     "ORD017": {"guest_name": "Mai Van R", "status": "processing", "time": "2026-09-14 10:05", "money": 199000},
#     "ORD018": {"guest_name": "Dinh Thi S", "status": "shipped", "time": "2026-09-13 16:50", "money": 275000},
#     "ORD019": {"guest_name": "Phung Van T", "status": "pending", "time": "2026-09-14 12:45", "money": 310000},
#     "ORD020": {"guest_name": "Chau Thi U", "status": "delivered", "time": "2026-09-07 19:30", "money": 550000}
# }
# app = Flask(__name__)
# @app.route("/orders/<order_id>", methods = ["DELETE"])
# def delete_order(order_id):
#     order = ORDERS.get(order_id)
#     if order is None:
#         return {"error" : "Not Found"}, 404
#     if order["status"] in ("shipped", "delivered"):
#         return {"error": "Cannot Delete"}, 409
#     ORDERS.pop(order_id, None)
#     return "", 204
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True)

# Bai 6
# from flask import Flask, jsonify, request
# app = Flask(__name__)
# _next = 1
# STUDENTS = [
#     {"id": 240001, "name": "Pham Tuan Linh", "class": "CS52", "gpa": 3.55},
#     {"id": 240002, "name": "Ngo Thanh Kien", "class": "CS51", "gpa": 3.16},
#     {"id": 240003, "name": "Bui Tuan A", "class": "IT101", "gpa": 2.11},
#     {"id": 240004, "name": "Nguyen Thanh B", "class": "CS51", "gpa": 3.81},
#     {"id": 240005, "name": "Ngo Thi Binh", "class": "IT101", "gpa": 2.6},
#     {"id": 240006, "name": "Ngo Thi A", "class": "CS52", "gpa": 2.83},
#     {"id": 240007, "name": "Nguyen Huu Nam", "class": "CS51", "gpa": 2.73},
#     {"id": 240008, "name": "Nguyen Thi An", "class": "CS52", "gpa": 3.06},
#     {"id": 240009, "name": "Le Duc Linh", "class": "SE100", "gpa": 2.42},
#     {"id": 240010, "name": "Nguyen Thanh Linh", "class": "CS51", "gpa": 2.08},
#     {"id": 240011, "name": "Hoang Huu Binh", "class": "SE100", "gpa": 2.67},
#     {"id": 240012, "name": "Pham Van Long", "class": "CS51", "gpa": 2.13},
#     {"id": 240013, "name": "Dang Ngoc Linh", "class": "CS52", "gpa": 3.53},
#     {"id": 240014, "name": "Bui Van Nam", "class": "CS52", "gpa": 3.34},
#     {"id": 240015, "name": "Pham Quang A", "class": "IT101", "gpa": 3.78},
#     {"id": 240016, "name": "Tran Ngoc Mai", "class": "CS52", "gpa": 2.91},
#     {"id": 240017, "name": "Dang Tuan Long", "class": "SE100", "gpa": 3.69},
#     {"id": 240018, "name": "Le Thu Long", "class": "SE100", "gpa": 3.7},
#     {"id": 240019, "name": "Tran Duc Dung", "class": "IT101", "gpa": 3.79},
#     {"id": 240020, "name": "Bui Tuan Dung", "class": "SE100", "gpa": 3.33},
#     {"id": 240021, "name": "Do Tuan Long", "class": "CS51", "gpa": 3.47},
#     {"id": 240022, "name": "Vu Van Mai", "class": "CS50", "gpa": 3.38},
#     {"id": 240023, "name": "Vu Quang Nam", "class": "CS50", "gpa": 2.06},
#     {"id": 240024, "name": "Do Minh C", "class": "CS52", "gpa": 3.18},
#     {"id": 240025, "name": "Pham Quang Linh", "class": "SE100", "gpa": 3.82},
#     {"id": 240026, "name": "Ngo Thu Lam", "class": "CS52", "gpa": 3.53},
#     {"id": 240027, "name": "Bui Minh C", "class": "SE100", "gpa": 2.31},
#     {"id": 240028, "name": "Do Ngoc Mai", "class": "CS52", "gpa": 3.14},
#     {"id": 240029, "name": "Hoang Thanh Kien", "class": "CS50", "gpa": 3.83},
#     {"id": 240030, "name": "Vu Thu Nam", "class": "CS51", "gpa": 3.24},
#     {"id": 240031, "name": "Nguyen Thu Nam", "class": "CS50", "gpa": 3.24},
#     {"id": 240032, "name": "Pham Tuan Long", "class": "CS50", "gpa": 2.44},
#     {"id": 240033, "name": "Hoang Ngoc Linh", "class": "CS50", "gpa": 3.07},
#     {"id": 240034, "name": "Pham Quang Kien", "class": "SE100", "gpa": 2.33},
#     {"id": 240035, "name": "Bui Van C", "class": "SE100", "gpa": 2.55},
#     {"id": 240036, "name": "Le Thu Chau", "class": "CS51", "gpa": 2.04},
#     {"id": 240037, "name": "Nguyen Ngoc Mai", "class": "CS50", "gpa": 3.57},
#     {"id": 240038, "name": "Pham Thi B", "class": "CS51", "gpa": 3.29},
#     {"id": 240039, "name": "Vu Ngoc Nam", "class": "IT101", "gpa": 3.0},
#     {"id": 240040, "name": "Pham Quang Long", "class": "IT101", "gpa": 2.27},
#     {"id": 240041, "name": "Do Thu Nam", "class": "SE100", "gpa": 2.38},
#     {"id": 240042, "name": "Pham Quang A", "class": "CS51", "gpa": 2.61},
#     {"id": 240043, "name": "Do Thu Binh", "class": "IT101", "gpa": 3.05},
#     {"id": 240044, "name": "Tran Van Kien", "class": "CS50", "gpa": 3.33},
#     {"id": 240045, "name": "Do Thu Linh", "class": "IT101", "gpa": 2.19},
#     {"id": 240046, "name": "Vu Van Lam", "class": "CS50", "gpa": 3.63},
#     {"id": 240047, "name": "Do Ngoc Mai", "class": "CS50", "gpa": 2.39},
#     {"id": 240048, "name": "Le Huu Binh", "class": "SE100", "gpa": 3.8},
#     {"id": 240049, "name": "Do Tuan B", "class": "CS52", "gpa": 2.43},
#     {"id": 240050, "name": "Do Huu C", "class": "IT101", "gpa": 3.91},
#     {"id": 240051, "name": "Vu Van Mai", "class": "CS51", "gpa": 2.71},
#     {"id": 240052, "name": "Do Tuan Nam", "class": "CS51", "gpa": 3.09},
#     {"id": 240053, "name": "Dang Huu Mai", "class": "SE100", "gpa": 2.13},
#     {"id": 240054, "name": "Nguyen Minh Nam", "class": "IT101", "gpa": 2.15},
#     {"id": 240055, "name": "Pham Thi A", "class": "IT101", "gpa": 3.54},
#     {"id": 240056, "name": "Ngo Minh A", "class": "CS52", "gpa": 2.45},
#     {"id": 240057, "name": "Dang Thi Kien", "class": "SE100", "gpa": 3.99},
#     {"id": 240058, "name": "Ngo Duc Dung", "class": "CS51", "gpa": 3.19},
#     {"id": 240059, "name": "Pham Duc Binh", "class": "CS50", "gpa": 2.98},
#     {"id": 240060, "name": "Hoang Thanh Anh", "class": "IT101", "gpa": 2.6},
#     {"id": 240061, "name": "Dang Minh Dung", "class": "CS52", "gpa": 2.75},
#     {"id": 240062, "name": "Vu Thanh Linh", "class": "CS50", "gpa": 3.38},
#     {"id": 240063, "name": "Tran Quang Binh", "class": "IT101", "gpa": 2.76},
#     {"id": 240064, "name": "Nguyen Huu Linh", "class": "CS52", "gpa": 2.81},
#     {"id": 240065, "name": "Ngo Thanh B", "class": "CS50", "gpa": 3.11},
#     {"id": 240066, "name": "Bui Thu Linh", "class": "CS52", "gpa": 3.91},
#     {"id": 240067, "name": "Pham Tuan Binh", "class": "SE100", "gpa": 2.1},
#     {"id": 240068, "name": "Vu Tuan B", "class": "CS52", "gpa": 3.58},
#     {"id": 240069, "name": "Le Van C", "class": "CS50", "gpa": 3.18},
#     {"id": 240070, "name": "Nguyen Thu C", "class": "CS52", "gpa": 2.07},
#     {"id": 240071, "name": "Dang Van Anh", "class": "CS51", "gpa": 3.63},
#     {"id": 240072, "name": "Le Van Mai", "class": "SE100", "gpa": 3.88},
#     {"id": 240073, "name": "Vu Quang Nam", "class": "CS50", "gpa": 3.54},
#     {"id": 240074, "name": "Vu Ngoc Linh", "class": "CS51", "gpa": 2.84},
#     {"id": 240075, "name": "Hoang Quang B", "class": "CS50", "gpa": 3.87},
#     {"id": 240076, "name": "Ngo Minh Mai", "class": "SE100", "gpa": 3.1},
#     {"id": 240077, "name": "Tran Huu A", "class": "CS51", "gpa": 3.59},
#     {"id": 240078, "name": "Le Duc Binh", "class": "CS52", "gpa": 3.89},
#     {"id": 240079, "name": "Bui Quang Anh", "class": "CS52", "gpa": 3.77},
#     {"id": 240080, "name": "Nguyen Van Long", "class": "CS50", "gpa": 3.97},
#     {"id": 240081, "name": "Le Van An", "class": "CS51", "gpa": 2.55},
#     {"id": 240082, "name": "Do Van A", "class": "SE100", "gpa": 2.83},
#     {"id": 240083, "name": "Ngo Van An", "class": "CS51", "gpa": 2.75},
#     {"id": 240084, "name": "Tran Minh Linh", "class": "CS50", "gpa": 3.7},
#     {"id": 240085, "name": "Le Thu C", "class": "CS52", "gpa": 3.65},
#     {"id": 240086, "name": "Dang Thanh Kien", "class": "CS52", "gpa": 2.13},
#     {"id": 240087, "name": "Do Van An", "class": "CS52", "gpa": 2.99},
#     {"id": 240088, "name": "Hoang Huu Anh", "class": "CS50", "gpa": 2.0},
#     {"id": 240089, "name": "Pham Tuan Linh", "class": "CS50", "gpa": 3.83},
#     {"id": 240090, "name": "Hoang Ngoc Nam", "class": "SE100", "gpa": 3.85},
#     {"id": 240091, "name": "Ngo Thi Binh", "class": "IT101", "gpa": 3.81},
#     {"id": 240092, "name": "Vu Thu Dung", "class": "CS52", "gpa": 2.53},
#     {"id": 240093, "name": "Ngo Quang Nam", "class": "IT101", "gpa": 2.56},
#     {"id": 240094, "name": "Bui Tuan Lam", "class": "CS50", "gpa": 2.75},
#     {"id": 240095, "name": "Dang Thanh Mai", "class": "CS52", "gpa": 2.72},
#     {"id": 240096, "name": "Do Thanh B", "class": "IT101", "gpa": 2.79},
#     {"id": 240097, "name": "Dang Duc Nam", "class": "CS50", "gpa": 2.85},
#     {"id": 240098, "name": "Do Tuan A", "class": "CS51", "gpa": 3.72},
#     {"id": 240099, "name": "Tran Tuan Kien", "class": "CS51", "gpa": 2.37},
#     {"id": 240100, "name": "Nguyen Thu B", "class": "SE100", "gpa": 3.34},
#     {"id": 240101, "name": "Vu Quang C", "class": "CS52", "gpa": 2.72},
#     {"id": 240102, "name": "Tran Van Long", "class": "CS51", "gpa": 2.77},
#     {"id": 240103, "name": "Le Ngoc An", "class": "CS51", "gpa": 3.57},
#     {"id": 240104, "name": "Le Thu Binh", "class": "CS50", "gpa": 2.75},
#     {"id": 240105, "name": "Pham Ngoc A", "class": "CS50", "gpa": 3.1},
#     {"id": 240106, "name": "Pham Quang Long", "class": "CS52", "gpa": 2.27},
#     {"id": 240107, "name": "Tran Ngoc Chau", "class": "SE100", "gpa": 3.72},
#     {"id": 240108, "name": "Vu Thu A", "class": "CS50", "gpa": 2.97},
#     {"id": 240109, "name": "Le Thu Nam", "class": "SE100", "gpa": 3.55},
#     {"id": 240110, "name": "Nguyen Quang C", "class": "CS50", "gpa": 3.31},
#     {"id": 240111, "name": "Nguyen Thi Anh", "class": "SE100", "gpa": 3.77},
#     {"id": 240112, "name": "Vu Minh Mai", "class": "CS50", "gpa": 3.65},
#     {"id": 240113, "name": "Dang Quang Chau", "class": "IT101", "gpa": 3.99},
#     {"id": 240114, "name": "Nguyen Minh Anh", "class": "IT101", "gpa": 3.22},
#     {"id": 240115, "name": "Le Thanh An", "class": "CS52", "gpa": 3.72},
#     {"id": 240116, "name": "Do Van Binh", "class": "IT101", "gpa": 2.86},
#     {"id": 240117, "name": "Bui Tuan Linh", "class": "CS52", "gpa": 3.42},
#     {"id": 240118, "name": "Hoang Thanh Dung", "class": "CS52", "gpa": 3.62},
#     {"id": 240119, "name": "Do Thanh Anh", "class": "SE100", "gpa": 2.67},
#     {"id": 240120, "name": "Le Minh Kien", "class": "IT101", "gpa": 2.5},
#     {"id": 240121, "name": "Vu Quang Anh", "class": "CS50", "gpa": 3.82},
#     {"id": 240122, "name": "Le Ngoc Chau", "class": "SE100", "gpa": 2.42},
#     {"id": 240123, "name": "Ngo Thu C", "class": "CS52", "gpa": 2.13},
#     {"id": 240124, "name": "Dang Huu A", "class": "IT101", "gpa": 3.09},
#     {"id": 240125, "name": "Do Ngoc Binh", "class": "CS51", "gpa": 3.09},
#     {"id": 240126, "name": "Nguyen Ngoc Anh", "class": "CS52", "gpa": 3.97},
#     {"id": 240127, "name": "Do Van Lam", "class": "CS52", "gpa": 2.17},
#     {"id": 240128, "name": "Ngo Tuan Mai", "class": "IT101", "gpa": 3.36},
#     {"id": 240129, "name": "Vu Duc B", "class": "SE100", "gpa": 3.72},
#     {"id": 240130, "name": "Pham Minh Binh", "class": "IT101", "gpa": 2.9},
#     {"id": 240131, "name": "Do Thi Nam", "class": "IT101", "gpa": 3.95},
#     {"id": 240132, "name": "Bui Thi Kien", "class": "CS50", "gpa": 2.38},
#     {"id": 240133, "name": "Ngo Van Mai", "class": "SE100", "gpa": 3.04},
#     {"id": 240134, "name": "Pham Thi B", "class": "SE100", "gpa": 2.06},
#     {"id": 240135, "name": "Pham Ngoc Long", "class": "CS51", "gpa": 2.02},
#     {"id": 240136, "name": "Do Van An", "class": "SE100", "gpa": 3.78},
#     {"id": 240137, "name": "Nguyen Ngoc Kien", "class": "CS52", "gpa": 3.28},
#     {"id": 240138, "name": "Ngo Thanh Linh", "class": "CS51", "gpa": 2.01},
#     {"id": 240139, "name": "Pham Duc A", "class": "IT101", "gpa": 2.88},
#     {"id": 240140, "name": "Bui Huu Lam", "class": "SE100", "gpa": 3.05},
#     {"id": 240141, "name": "Pham Quang Chau", "class": "CS50", "gpa": 2.91},
#     {"id": 240142, "name": "Bui Duc C", "class": "CS50", "gpa": 3.58},
#     {"id": 240143, "name": "Ngo Van Chau", "class": "SE100", "gpa": 3.15},
#     {"id": 240144, "name": "Bui Thi Kien", "class": "IT101", "gpa": 3.61},
#     {"id": 240145, "name": "Nguyen Quang B", "class": "CS50", "gpa": 2.02},
#     {"id": 240146, "name": "Nguyen Thu Anh", "class": "SE100", "gpa": 2.75},
#     {"id": 240147, "name": "Do Ngoc Long", "class": "CS52", "gpa": 2.91},
#     {"id": 240148, "name": "Nguyen Tuan B", "class": "SE100", "gpa": 3.79},
#     {"id": 240149, "name": "Pham Tuan An", "class": "CS51", "gpa": 2.19},
#     {"id": 240150, "name": "Dang Ngoc Long", "class": "IT101", "gpa": 2.08},
#     {"id": 240151, "name": "Dang Thanh Chau", "class": "CS52", "gpa": 3.95},
#     {"id": 240152, "name": "Tran Ngoc Chau", "class": "CS50", "gpa": 2.74},
#     {"id": 240153, "name": "Pham Thu Kien", "class": "SE100", "gpa": 3.36},
#     {"id": 240154, "name": "Tran Huu An", "class": "CS51", "gpa": 2.34},
#     {"id": 240155, "name": "Pham Thu An", "class": "SE100", "gpa": 3.27},
#     {"id": 240156, "name": "Le Ngoc An", "class": "IT101", "gpa": 2.34},
#     {"id": 240157, "name": "Ngo Duc Binh", "class": "IT101", "gpa": 2.64},
#     {"id": 240158, "name": "Tran Thi B", "class": "CS50", "gpa": 3.83},
#     {"id": 240159, "name": "Hoang Tuan Long", "class": "CS52", "gpa": 2.41},
#     {"id": 240160, "name": "Dang Ngoc Anh", "class": "CS52", "gpa": 2.52},
#     {"id": 240161, "name": "Hoang Duc Lam", "class": "SE100", "gpa": 3.51},
#     {"id": 240162, "name": "Bui Van Long", "class": "IT101", "gpa": 3.06},
#     {"id": 240163, "name": "Hoang Thu Long", "class": "CS52", "gpa": 2.8},
#     {"id": 240164, "name": "Bui Van Kien", "class": "CS52", "gpa": 2.57},
#     {"id": 240165, "name": "Pham Huu Linh", "class": "SE100", "gpa": 2.25},
#     {"id": 240166, "name": "Vu Huu Nam", "class": "IT101", "gpa": 2.62},
#     {"id": 240167, "name": "Vu Van Anh", "class": "SE100", "gpa": 2.72},
#     {"id": 240168, "name": "Hoang Thu Dung", "class": "CS52", "gpa": 3.75},
#     {"id": 240169, "name": "Do Van Chau", "class": "IT101", "gpa": 3.21},
#     {"id": 240170, "name": "Tran Thi Linh", "class": "CS51", "gpa": 2.93},
#     {"id": 240171, "name": "Pham Tuan An", "class": "CS50", "gpa": 3.71},
#     {"id": 240172, "name": "Hoang Ngoc Lam", "class": "IT101", "gpa": 2.17},
#     {"id": 240173, "name": "Hoang Duc C", "class": "CS50", "gpa": 2.2},
#     {"id": 240174, "name": "Dang Thi Long", "class": "CS51", "gpa": 3.65},
#     {"id": 240175, "name": "Nguyen Minh Lam", "class": "CS52", "gpa": 3.75},
#     {"id": 240176, "name": "Nguyen Thanh Dung", "class": "IT101", "gpa": 2.99},
#     {"id": 240177, "name": "Vu Thanh Lam", "class": "CS52", "gpa": 3.44},
#     {"id": 240178, "name": "Pham Ngoc Linh", "class": "SE100", "gpa": 3.2},
#     {"id": 240179, "name": "Do Quang Mai", "class": "CS52", "gpa": 3.89},
#     {"id": 240180, "name": "Le Tuan Long", "class": "CS52", "gpa": 2.05},
#     {"id": 240181, "name": "Nguyen Van Kien", "class": "CS51", "gpa": 3.82},
#     {"id": 240182, "name": "Tran Thanh Mai", "class": "CS51", "gpa": 2.37},
#     {"id": 240183, "name": "Pham Quang An", "class": "CS51", "gpa": 2.12},
#     {"id": 240184, "name": "Ngo Quang A", "class": "CS52", "gpa": 3.58},
#     {"id": 240185, "name": "Hoang Thu Nam", "class": "IT101", "gpa": 3.92},
#     {"id": 240186, "name": "Dang Ngoc Linh", "class": "CS50", "gpa": 2.15},
#     {"id": 240187, "name": "Ngo Huu Lam", "class": "CS50", "gpa": 3.81},
#     {"id": 240188, "name": "Bui Van Anh", "class": "SE100", "gpa": 2.69},
#     {"id": 240189, "name": "Pham Thanh Chau", "class": "SE100", "gpa": 2.51},
#     {"id": 240190, "name": "Nguyen Thi Kien", "class": "IT101", "gpa": 2.7},
#     {"id": 240191, "name": "Bui Van A", "class": "IT101", "gpa": 3.91},
#     {"id": 240192, "name": "Hoang Tuan B", "class": "SE100", "gpa": 2.27},
#     {"id": 240193, "name": "Ngo Thi Linh", "class": "SE100", "gpa": 2.72},
#     {"id": 240194, "name": "Tran Minh Binh", "class": "CS51", "gpa": 2.14},
#     {"id": 240195, "name": "Vu Tuan Chau", "class": "CS51", "gpa": 2.11},
#     {"id": 240196, "name": "Dang Ngoc Long", "class": "CS50", "gpa": 2.48},
#     {"id": 240197, "name": "Le Huu Linh", "class": "CS52", "gpa": 3.61},
#     {"id": 240198, "name": "Hoang Quang Mai", "class": "CS51", "gpa": 2.42},
#     {"id": 240199, "name": "Dang Van Long", "class": "CS50", "gpa": 2.49},
#     {"id": 240200, "name": "Nguyen Thanh Anh", "class": "IT101", "gpa": 2.63},
# ]

# def find(sid):
#     return next((s for s in STUDENTS if s["id"] == sid), None)

# @app.route("/students", methods=["GET"])
# def list_students():
#     limit = int(request.args.get("limit", 100))
#     query = request.args.get("query", "").strip().lower()
#     sort = request.args.get("sort", "").strip().lower()
#     min_gpa = request.args.get("mingpa")
#     students = [s for s in STUDENTS if query in s["name"].lower()]

#     if min_gpa:
#         try:
#             val = float(min_gpa)
#             students = [s for s in students if s.get("gpa", 0.0) >= val]
#         except ValueError:
#             return {"error": "min_gpa must be a valid number"}, 400

#     if sort == "gpa":
#         students = sorted(students, key=lambda x: x["gpa"])
#     elif sort== "-gpa":
#         students = sorted(students, key=lambda x: x["gpa"], reverse=True)
#     students = students[:limit]
    
#     return jsonify({"students": students}), 200

# @app.route("/students/<int:sid>", methods=["GET"])
# def get_s(sid):
#     student = find(sid)
#     if not student:
#         return {"Error" : "Not Found"}, 404
#     return jsonify(student), 200

# @app.route("/students", methods=["POST"])
# def insert_student():
#     global _next
#     body = request.get_json(silent=True) or {}
#     n, c = body.get("name"), body.get("class")
#     if not n or not c:
#         return {"error": "need name+class"}, 400
#     student = {"id": _next, "name": n, "class": c}
#     _next += 1; STUDENTS.append(student)
#     return jsonify(student), 201, {"Location":f"/students/{student['id']}"}

# @app.route("/students/<int:sid>", methods=["PUT", "DELETE"])
# def modify_s(sid):
#     student = find(sid)
#     if not student: 
#         return {"error":"not found"}, 404
#     if request.method == "PUT":
#         student.update(request.get_json(silent=True) or {})
#         return jsonify(student), 200
#     STUDENTS.remove(student)
#     return"" , 204
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True )


#Bai 1

# app.py — bài 1: GET /books, POST /books
# from flask import Flask, jsonify, request, make_response
# app = Flask(__name__)
# BOOKS = []
# _next_id = 1
# # ─── GET /books —— trả danh sách
# @app.get("/books")
# def list_books():
#     return jsonify({"data": BOOKS,"total": len(BOOKS)}), 200
# # ─── POST /books —— tạo mới
# @app.post("/books")
# def create_book():
#     global _next_id
#     if not request.is_json:
#         return jsonify(error="expected JSON"), 415
#     p = request.get_json(silent=True)
#     if p is None:
#         return jsonify(error="JSON is required"), 400
#     if not isinstance(p, dict):
#         return jsonify(error="wrong is required"), 400
#     t = (p.get("title") or"").strip()
#     a = (p.get("author") or"").strip()
#     if not t or not a:
#         return jsonify(error="title and author required"), 422
#     if not t and a:
#         return jsonify(error="wrong json type"), 400
#     book = {"id": _next_id, "title": t, "author": a}
#     BOOKS.append(book); _next_id += 1
#     resp = make_response(jsonify(book), 201)
#     resp.headers["Location"] = f"/books/{book['id']}"
#     return resp
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port = 5000, debug = True)

#Bai 2

# from flask import Flask, jsonify, request, make_response
# app = Flask(__name__)
# BOOKS = []


# _next_id = 1
# # ─── GET /books —— trả danh sách
# @app.get("/books")
# def list_books():
#     return jsonify({"data": BOOKS,"total": len(BOOKS)}), 200
# # ─── POST /books —— tạo mới
# @app.post("/books")
# def create_book():
#     global _next_id
#     if not request.is_json:
#         return jsonify(error="expected JSON"), 415
#     p = request.get_json(silent=True)
#     if p is None:
#         return jsonify(error="JSON is required"), 400
#     if not isinstance(p, dict):
#         return jsonify(error="JSON body must be object"), 400
#     t = (p.get("title") or"").strip()
#     a = (p.get("author") or"").strip()
#     if not t or not a:
#         return jsonify(error="title and author required"), 422
#     book = {"id": _next_id, "title": t, "author": a}
#     BOOKS.append(book); _next_id += 1
#     resp = make_response(jsonify(book), 201)
#     resp.headers["Location"] = f"/books/{book['id']}"
#     return resp

# @app.get("/books/<int:bid>")
# def fetch(bid):
#     i = next((k for k,b in enumerate(BOOKS) if b["id"]==bid), None)
#     if i is None: 
#         return jsonify(error="not found"), 404
#     resp = make_response(jsonify(BOOKS[i]), 200)
#     resp.headers["Cache-Control"]="max-age=60"; return resp
# # ─── PUT ─── thay toàn bộ, title+author bắt buộc
# @app.put("/books/<int:bid>")
# def put(bid):
#     p = request.get_json(silent=True) or {}
#     t,a = p.get("title"), p.get("author")
#     if not t or not a: 
#         return jsonify(error="need title+author"), 422
#     i = next((k for k,b in enumerate(BOOKS) if b["id"]==bid), None)
#     new_book = {"id":bid,"title":t.strip(),"author":a.strip(),
#               "isbn":p.get("isbn"),"price":p.get("price")}
#     if i is None:
#         BOOKS.append(new_book)
#         return jsonify(new_book), 201
#     else:
#         BOOKS[i] = new_book
#         return jsonify(BOOKS[i]), 200
#     # ─── PATCH ─── chỉ cập nhật field có trong body
# @app.patch("/books/<int:bid>")
# def patch(bid):
#     i = next((k for k,b in enumerate(BOOKS) if b["id"]==bid), None)
#     if i is None: 
#         return jsonify(error="not found"), 404
#     p = request.get_json(silent=True) or {}
#     if p.get("price", 0) < 0:
#         return jsonify(error="price must be positive"), 422
#     for k in"title author isbn price".split():
#         if k in p: 
#             BOOKS[i][k] = p[k]
#             return jsonify(BOOKS[i]), 200
#     # ─── DELETE ─── idempotent, trả 204
# @app.delete("/books/<int:bid>")
# def delete(bid):
#     i = next((k for k,b in enumerate(BOOKS)
#     if b["id"]==bid), None)
#     if i is None: 
#         return jsonify(error="not found"), 404
#     BOOKS.pop(i); 
#     return"", 204

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port = 5000, debug = True)

#Bai 3
# app.py — GET /books nâng cấp với pagination + filter + HATEOAS
from flask import Flask, jsonify, request, make_response
app = Flask(__name__)
# ─── tham số phân trang
DEFAULT_SIZE, MAX_SIZE = 20, 100
BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "Clean Architecture", "author": "Robert C. Martin"},
    {"id": 3, "title": "1984", "author": "Orwell"},
    {"id": 4, "title": "Animal Farm", "author": "Orwell"},
    {"id": 5, "title": "The Pragmatic Programmer", "author": "Andrew Hunt, David Thomas"},
    {"id": 6, "title": "Refactoring", "author": "Martin Fowler"},
    {"id": 7, "title": "Design Patterns", "author": "Erich Gamma et al."},
    {"id": 8, "title": "Introduction to Algorithms", "author": "Thomas H. Cormen"},
    {"id": 9, "title": "The Mythical Man-Month", "author": "Frederick P. Brooks Jr."},
    {"id": 10, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 11, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 12, "title": "Brave New World", "author": "Aldous Huxley"},
    {"id": 13, "title": "The Catcher in the Rye", "author": "J.D. Salinger"},
    {"id": 14, "title": "Crime and Punishment", "author": "Fyodor Dostoevsky"},
    {"id": 15, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"id": 16, "title": "Dune", "author": "Frank Herbert"},
    {"id": 17, "title": "Fahrenheit 451", "author": "Ray Bradbury"},
    {"id": 18, "title": "Atomic Habits", "author": "James Clear"},
    {"id": 19, "title": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari"},
    {"id": 20, "title": "Thinking, Fast and Slow", "author": "Daniel Kahneman"},
]
# ─── list + filter + paginate + links
@app.get("/books")
def list_books():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify(error="page and size must be int"), 400
    page = max(page, 1)
    size = max(min(size, MAX_SIZE), 1)
    # filter: author chính xác, q tìm trong title
    flt = BOOKS
    a = request.args.get("author")
    if a: 
        flt = [b for b in flt if b["author"].lower()==a.lower()]
    q = (request.args.get("q")or"").lower()
    if q: 
        flt = [b for b in flt if q in b["title"].lower()]
    # paginate
    total = len(flt)
    start=(page-1)*size
    end=start+size
    items = flt[start:end]
    last=(total+size-1) //size
    # HATEOAS links
    def u(p): 
        return f"/books?page={p}&size={size}"
    links = {
            "self":{"href":u(page)},
            "first":{"href":u(1)},
            "last":{"href":u(max(last,1))}}
    if page > 1: links["prev"]={"href":u(page-1)}
    if end < total: links["next"]={"href":u(page+1)}
    body = {"data":items,
    "pagination":{"page":page,"size":size,"total":total,"total_pages":last},
    "_links":links}
    resp = make_response(jsonify(body), 200)
    resp.headers["Cache-Control"]="public, max-age=30"
    return resp
if __name__ == "__main__":
    app.run(host="127.0.0.1", port = 5000, debug = True)