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
# from flask import Flask, jsonify, request, make_response
# app = Flask(__name__)
# # ─── tham số phân trang
# DEFAULT_SIZE, MAX_SIZE = 20, 100
# BOOKS = [
#     {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
#     {"id": 2, "title": "Clean Architecture", "author": "Robert C. Martin"},
#     {"id": 3, "title": "1984", "author": "Orwell"},
#     {"id": 4, "title": "Animal Farm", "author": "Orwell"},
#     {"id": 5, "title": "The Pragmatic Programmer", "author": "Andrew Hunt, David Thomas"},
#     {"id": 6, "title": "Refactoring", "author": "Martin Fowler"},
#     {"id": 7, "title": "Design Patterns", "author": "Erich Gamma et al."},
#     {"id": 8, "title": "Introduction to Algorithms", "author": "Thomas H. Cormen"},
#     {"id": 9, "title": "The Mythical Man-Month", "author": "Frederick P. Brooks Jr."},
#     {"id": 10, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
#     {"id": 11, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
#     {"id": 12, "title": "Brave New World", "author": "Aldous Huxley"},
#     {"id": 13, "title": "The Catcher in the Rye", "author": "J.D. Salinger"},
#     {"id": 14, "title": "Crime and Punishment", "author": "Fyodor Dostoevsky"},
#     {"id": 15, "title": "The Hobbit", "author": "J.R.R. Tolkien"},
#     {"id": 16, "title": "Dune", "author": "Frank Herbert"},
#     {"id": 17, "title": "Fahrenheit 451", "author": "Ray Bradbury"},
#     {"id": 18, "title": "Atomic Habits", "author": "James Clear"},
#     {"id": 19, "title": "Sapiens: A Brief History of Humankind", "author": "Yuval Noah Harari"},
#     {"id": 20, "title": "Thinking, Fast and Slow", "author": "Daniel Kahneman"},
# ]
# # ─── list + filter + paginate + links
# @app.get("/books")
# def list_books():
#     try:
#         page = int(request.args.get("page", 1))
#         size = int(request.args.get("size", DEFAULT_SIZE))
#     except ValueError:
#         return jsonify(error="page and size must be int"), 400
#     page = max(page, 1)
#     size = max(min(size, MAX_SIZE), 1)
#     # filter: author chính xác, q tìm trong title
#     flt = BOOKS
#     a = request.args.get("author")
#     if a: 
#         flt = [b for b in flt if b["author"].lower()==a.lower()]
#     q = (request.args.get("q")or"").lower()
#     if q: 
#         flt = [b for b in flt if q in b["title"].lower()]
#     # paginate
#     total = len(flt)
#     start=(page-1)*size
#     end=start+size
#     items = flt[start:end]
#     last=(total+size-1) //size
#     # HATEOAS links
#     def u(p): 
#         return f"/books?page={p}&size={size}"
#     links = {
#             "self":{"href":u(page)},
#             "first":{"href":u(1)},
#             "last":{"href":u(max(last,1))}}
#     if page > 1: links["prev"]={"href":u(page-1)}
#     if end < total: links["next"]={"href":u(page+1)}
#     body = {"data":items,
#     "pagination":{"page":page,"size":size,"total":total,"total_pages":last},
#     "_links":links}
#     resp = make_response(jsonify(body), 200)
#     resp.headers["Cache-Control"]="public, max-age=30"
#     return resp
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port = 5000, debug = True)

# import sqlite3

# conn = sqlite3.connect("database.db")
# cur = conn.cursor()

# # Tạo bảng books
# cur.execute("""
# CREATE TABLE IF NOT EXISTS books (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title TEXT NOT NULL,
#     author TEXT NOT NULL
# )
# """)

# # Tạo bảng orders
# cur.execute("""
# CREATE TABLE IF NOT EXISTS orders (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     customer_name TEXT NOT NULL,
#     total_amount REAL NOT NULL,
#     status TEXT NOT NULL
# )
# """)

# # Chèn dữ liệu mẫu
# cur.executemany("INSERT INTO books (title, author) VALUES (?, ?)", [
#     ("Clean Code", "Robert C. Martin"),
#     ("Clean Architecture", "Robert C. Martin"),
#     ("1984", "Orwell"),
#     ("Animal Farm", "Orwell"),
#     ("Design Patterns", "GoF")
# ])

# cur.executemany("INSERT INTO orders (customer_name, total_amount, status) VALUES (?, ?, ?)", [
#     ("Nguyen Van A", 45.5, "completed"),
#     ("Tran Thi B", 120.0, "pending")
# ])

# conn.commit()
# conn.close()
# print("Khởi tạo database thành công!")


import sqlite3
from flask import Flask, jsonify, request, make_response

app = Flask(__name__)
DEFAULT_SIZE, MAX_SIZE = 20, 100

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row  # Trả về dạng dict-like thay vì tuple
    return conn

# Endpoint GET /books với SQLite
@app.get("/books")
def list_books():
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", DEFAULT_SIZE))
    except ValueError:
        return jsonify(error="page and size must be int"), 400

    page = max(page, 1)
    size = max(min(size, MAX_SIZE), 1)

    author = request.args.get("author")
    q = request.args.get("q")

    conn = get_db_connection()
    cur = conn.cursor()

    # Xây dựng câu truy vấn động theo filter
    where_clauses = []
    params = []
    if author:
        where_clauses.append("LOWER(author) = LOWER(?)")
        params.append(author)
    if q:
        where_clauses.append("LOWER(title) LIKE LOWER(?)")
        params.append(f"%{q}%")

    where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    # 1. Đếm tổng số bản ghi
    total = cur.execute(f"SELECT COUNT(*) FROM books{where_sql}", params).fetchone()[0]

    # 2. Lấy dữ liệu theo LIMIT và OFFSET (Phân trang ở tầng DB)
    offset = (page - 1) * size
    query_sql = f"SELECT id, title, author FROM books{where_sql} LIMIT ? OFFSET ?"
    rows = cur.execute(query_sql, params + [size, offset]).fetchall()
    items = [dict(row) for row in rows]
    conn.close()

    last = (total + size - 1) // size if total > 0 else 1

    # Tạo HATEOAS links
    filter_params = ""
    if author: filter_params += f"&author={author}"
    if q: filter_params += f"&q={q}"

    def u(p): return f"/books?page={p}&size={size}{filter_params}"

    links = {
        "self": {"href": u(page)},
        "first": {"href": u(1)},
        "last": {"href": u(max(last, 1))}
    }
    if page > 1: links["prev"] = {"href": u(page - 1)}
    if offset + size < total: links["next"] = {"href": u(page + 1)}

    body = {
        "data": items,
        "pagination": {"page": page, "size": size, "total": total, "total_pages": last},
        "_links": links
    }

    resp = make_response(jsonify(body), 200)
    resp.headers["Cache-Control"] = "public, max-age=30"
    return resp

# Bổ sung GET /orders/<oid> theo yêu cầu đề bài
@app.get("/orders/<int:oid>")
def get_order(oid):
    conn = get_db_connection()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (oid,)).fetchone()
    conn.close()

    if order is None:
        return jsonify(error=f"Order {oid} not found"), 404

    order_dict = dict(order)
    return jsonify({
        "data": order_dict,
        "_links": {
            "self": {"href": f"/orders/{oid}"},
            "collection": {"href": "/orders"}
        }
    }), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)