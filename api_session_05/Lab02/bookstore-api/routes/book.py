import json
import base64
import binascii
from pathlib import Path
from flask import Blueprint, request, jsonify
from jsonschema import validate, ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, or_
from models import db, Book

books_bp = Blueprint("books", __name__, url_prefix="/api/v1/books")

schema_path = Path(__file__).resolve().parent.parent / "schemas" / "book.json"
book_schema = json.loads(schema_path.read_text(encoding="utf-8"))




@books_bp.get("/<int:id>")
def get_book(id):
    book = db.get_or_404(Book, id)
    return jsonify(book.to_dict())


@books_bp.get("")
def get_books():
    sort_raw = request.args.get("sort", "id")
    p, cols, desc = parse_sort(sort_raw)

    if p is None:
        return jsonify({"error": cols}), desc

    try:
        limit = int(request.args.get("limit", 20))
        cat_raw = request.args.get("category_id")
        cat_id = int(cat_raw) if cat_raw is not None else None
    except ValueError:
        return jsonify({"error": "bad_parameter"}), 400

    if not 1 <= limit <= 100:
        return jsonify({"error": "bad_limit"}), 400

    if cat_id is not None and cat_id <= 0:
        return jsonify({"error": "bad_category_id"}), 400

    q = db.select(Book)

    if cat_id is not None:
        q = q.where(Book.category_id == cat_id)

    q, error, status = apply_cursor(
        q, p, desc, request.args.get("cursor")
    )

    if error:
        return jsonify({"error": error}), status

    rows = db.session.execute(
        q.order_by(*cols).limit(limit + 1)
    ).scalars().all()

    return build_response(rows, limit, p)



@books_bp.post("")
def create_book():
    data = request.get_json(silent=True)
    try:
        validate(data, book_schema)
    except ValidationError as e:
        return jsonify({"error": e.message}), 400

    book = Book(**data)
    db.session.add(book)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "ISBN đã tồn tại hoặc khóa ngoại không hợp lệ"}), 409

    return jsonify(book.to_dict()), 201


@books_bp.route("/<int:id>", methods=["PUT", "PATCH"])
def update_book(id):
    book = db.get_or_404(Book, id)
    data = request.get_json(silent=True)

    schema = book_schema.copy()
    if request.method == "PATCH":
        schema["required"] = []

    try:
        validate(data, schema)
    except ValidationError as e:
        return jsonify({"error": e.message}), 400

    for key, value in data.items():
        setattr(book, key, value)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Dữ liệu trùng hoặc khóa ngoại không hợp lệ"}), 409

    return jsonify(book.to_dict())


@books_bp.delete("/<int:id>")
def delete_book(id):
    book = db.get_or_404(Book, id)
    db.session.delete(book)
    db.session.commit()
    return "", 204

#sắp xếp
SORT = {
    "id": Book.id,
    "price": Book.price_vnd
}


def parse_sort(raw):
    #Nhận đầu vào "-" là desc(giảm dần) và nhận biết ngoài key thì là lỗi
    desc = raw.startswith("-")
    key = raw.lstrip("-")

    if key not in SORT:
        return None, "bad_sort", 400
    p = SORT[key]
    cols = [p.desc() if desc else p.asc()]

    #-id là giảm dần theo cột và ngược lại id là tăng
    if key != "id":
        cols.append(Book.id.desc() if desc else Book.id.asc())
    return p, cols, desc


def apply_cursor(q, p, desc, token):
    if not token:
        return q, None, None

    try:
        raw = base64.urlsafe_b64decode(token + "=" * (-len(token) % 4))
        cursor = json.loads(raw)

        value = cursor["value"]
        last_id = cursor["id"]

        if type(value) is not int or type(last_id) is not int:
            return None, "bad_cursor", 400

    except (ValueError, KeyError, TypeError, binascii.Error):
        return None, "bad_cursor", 400

    if p.key == "id":
        condition = Book.id < last_id if desc else Book.id > last_id
    elif desc:
        condition = or_(
            p < value,
            and_(p == value, Book.id < last_id)
        )
    else:
        condition = or_(
            p > value,
            and_(p == value, Book.id > last_id)
        )

    return q.where(condition), None, None


def build_response(rows, limit, p):
    has_more = len(rows) > limit
    books = rows[:limit]
    next_cursor = None

    if has_more:
        last = books[-1]
        cursor = {
            "value": getattr(last, p.key),
            "id": last.id
        }
        next_cursor = base64.urlsafe_b64encode(
            json.dumps(cursor).encode()
        ).decode().rstrip("=")

    return jsonify({
        "items": [book.to_dict() for book in books],
        "next_cursor": next_cursor,
        "has_more": has_more
    }), 200



