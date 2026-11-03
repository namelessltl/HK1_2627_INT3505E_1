
import base64
import binascii
import json
import re
from sqlalchemy import and_, or_
from models import Book


SORT = {
    "id": Book.id,
    "price": Book.price_vnd,
    "title": Book.title,
    "stock": Book.stock,
}


def parse_sort(raw):
    """Return (sort_specs, error, status); error behavior matches slide's return style."""
    if not isinstance(raw, str) or not raw or len(raw) > 120:
        return None, "bad_sort", 400

    specs = []
    used = set()
    for part in raw.split(","):
        part = part.strip()
        desc = part.startswith("-")
        key = part[1:] if desc else part
        if key not in SORT or key in used:
            return None, "bad_sort", 400
        used.add(key)
        specs.append((key, desc))

    # Stable unique tie-breaker, even when prices/titles coincide.
    if "id" not in used:
        specs.append(("id", specs[-1][1]))

    return specs, None, None


def sort_columns(specs):
    return [SORT[key].desc() if desc else SORT[key].asc() for key, desc in specs]


def encode_cursor(book, specs, sort_raw, genre, category_id):
    data = {
        "sort": sort_raw,
        "genre": genre,
        "category_id": category_id,
        "values": [getattr(book, SORT[key].key) for key, _ in specs],
        "id": book.id,
    }
    return base64.urlsafe_b64encode(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).decode("ascii").rstrip("=")


def apply_cursor(query, specs, token, sort_raw, genre, category_id):
    """Use tuple-lexicographic comparison; reject cursor reused with new filters/sort."""
    if token is None:
        return query, None, None

    try:
        if len(token) > 4096 or re.fullmatch(r"[A-Za-z0-9_-]+", token) is None:
            return None, "bad_cursor", 400
        payload = base64.b64decode(
            token + "=" * (-len(token) % 4), altchars=b"-_", validate=True
        )
        data = json.loads(payload.decode("utf-8"))
        if not isinstance(data, dict):
            return None, "bad_cursor", 400
        if (
            data.get("sort") != sort_raw
            or data.get("genre") != genre
            or data.get("category_id") != category_id
        ):
            return None, "bad_cursor", 400
        values = data["values"]
        if not isinstance(values, list) or len(values) != len(specs):
            return None, "bad_cursor", 400
        for (key, _), value in zip(specs, values):
            expected_type = str if key == "title" else int
            if type(value) is not expected_type:
                return None, "bad_cursor", 400
        if type(data.get("id")) is not int:
            return None, "bad_cursor", 400
        for index, (key, _) in enumerate(specs):
            if key == "id" and values[index] != data["id"]:
                return None, "bad_cursor", 400
    except (ValueError, KeyError, TypeError, UnicodeError, binascii.Error):
        return None, "bad_cursor", 400

    # (k1 > v1) OR (k1 = v1 AND k2 > v2) ... ; descending uses '<'.
    branches = []
    for index, (key, desc) in enumerate(specs):
        prefix = [SORT[specs[j][0]] == values[j] for j in range(index)]
        col = SORT[key]
        comparison = col < values[index] if desc else col > values[index]
        branches.append(and_(*prefix, comparison))

    return query.where(or_(*branches)), None, None


def build_response(rows, limit, strategy, *, specs=None, sort_raw=None,
                   genre=None, category_id=None, offset=0):
    has_more = len(rows) > limit
    books = rows[:limit]
    response = {
        "strategy": strategy,
        "items": [book.to_dict() for book in books],
        "has_more": has_more,
        "next_cursor": None,
        "next_offset": None,
    }
    if has_more:
        if strategy == "cursor":
            response["next_cursor"] = encode_cursor(
                books[-1], specs, sort_raw, genre, category_id
            )
        else:
            response["next_offset"] = offset + limit
    return response
