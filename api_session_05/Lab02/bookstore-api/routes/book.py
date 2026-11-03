import json
from pathlib import Path
from flask import Blueprint, request, jsonify
from jsonschema import validate, ValidationError
from sqlalchemy.exc import IntegrityError
from models import db, Book, Category
from .pagination import apply_cursor, build_response, parse_sort, sort_columns

books_bp = Blueprint("books", __name__, url_prefix="/api/v1/books")

schema_path = Path(__file__).resolve().parent.parent / "schemas" / "book.json"
book_schema = json.loads(schema_path.read_text(encoding="utf-8"))




@books_bp.get("/<int:id>")
def get_book(id):
    book = db.get_or_404(Book, id)
    return jsonify(book.to_dict())


@books_bp.get("")
def get_books():
    strategy = request.args.get("strategy", "cursor")
    if strategy not in ("cursor", "offset"):
        return jsonify({"error": "bad_strategy"}), 400

    sort_raw = request.args.get("sort", "id")
    specs, error, status = parse_sort(sort_raw)
    if error:
        return jsonify({"error": error}), status

    try:
        limit = int(request.args.get("limit", 20))
        cat_raw = request.args.get("category_id")
        cat_id = int(cat_raw) if cat_raw is not None else None
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify({"error": "bad_parameter"}), 400

    if not 1 <= limit <= 100:
        return jsonify({"error": "bad_limit"}), 400

    if cat_id is not None and cat_id <= 0:
        return jsonify({"error": "bad_category_id"}), 400

    if offset < 0 or (strategy == "cursor" and offset != 0):
        return jsonify({"error": "bad_offset"}), 400

    genre = request.args.get("genre")
    if genre is not None:
        genre = genre.strip()
        if not genre or len(genre) > 100:
            return jsonify({"error": "bad_genre"}), 400

    cursor = request.args.get("cursor")
    if strategy == "offset" and cursor is not None:
        return jsonify({"error": "bad_cursor"}), 400

    q = db.select(Book)

    if cat_id is not None:
        q = q.where(Book.category_id == cat_id)

    if genre is not None:
        q = q.join(Book.category).where(Category.slug == genre)

    if strategy == "cursor":
        q, error, status = apply_cursor(
            q, specs, cursor, sort_raw, genre, cat_id
        )
        if error:
            return jsonify({"error": error}), status
    else:
        q = q.offset(offset)

    rows = db.session.execute(
        q.order_by(*sort_columns(specs)).limit(limit + 1)
    ).scalars().all()

    return jsonify(build_response(
        rows, limit, strategy, specs=specs, sort_raw=sort_raw,
        genre=genre, category_id=cat_id, offset=offset,
    )), 200



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
