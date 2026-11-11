"""LAB 1 — add your five tests here. Do not delete the smoke tests.

A. GET /books, empty database -> HTTP 200 and []
B. GET /books/9999 -> HTTP 404, JSON code == NOT_FOUND
C. POST /books with only author -> HTTP 400, errors contains title
D. POST valid book, DELETE it, GET same id -> HTTP 404
BONUS. Validate a Book response using JSON Schema; add an unknown
       field to a *copy* of the response and assert ValidationError.

Useful imports:
    from jsonschema import validate, ValidationError
    import pytest
    from tools import get_book_schema

Do not depend on test execution order. Fixtures: client, app, sample_book.
"""
from jsonschema import validate, ValidationError
import pytest
from tools import get_book_schema


@pytest.fixture()
def book_response(client, sample_book):
    response = client.get(f"/books/{sample_book}")
    assert response.status_code == 200
    assert response.is_json
    return response.get_json()


@pytest.fixture()
def book_response_with_extra_field(book_response):
    # Simulate a leaked field without changing the real response.
    data = book_response.copy()
    data["password_hash"] = "fake-password-hash-for-test"
    return data

# tests/test_list_books.py
def test_list_books_empty(client): 
    reponse = client.get("/books")
    assert reponse.status_code == 200
    assert reponse.content_type == "application/json"
    assert reponse.get_json() == []

def test_get_book_not_found(client):
    response = client.get("/books/9999")

    assert response.status_code == 404
    assert response.is_json
    assert response.get_json()["code"] == "NOT_FOUND"


def test_response_extra_field_blocked(book_response, book_response_with_extra_field):
    schema = get_book_schema()
    # Correct the intentional Lab 2 year defect in this test's schema only.
    schema["properties"]["year"]["type"] = "integer"
    # jsonschema uses null types rather than OpenAPI 3.0's nullable keyword.
    for property_schema in schema["properties"].values():
        if property_schema.pop("nullable", False):
            property_schema["type"] = [property_schema["type"], "null"]

    assert "password_hash" not in book_response
    validate(instance=book_response, schema=schema)

    with pytest.raises(ValidationError) as exc_info:
        validate(instance=book_response_with_extra_field, schema=schema)

    assert exc_info.value.validator == "additionalProperties"
    assert "password_hash" in exc_info.value.message


def test_create_book_missing_title(client):
    response = client.post("/books", json={"author": "J.J. Geewax"})

    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert data["code"] == "VALIDATION_ERROR"
    assert any(error["field"] == "title" for error in data["errors"])


def test_get_deleted_book_not_found(client):
    created = client.post(
        "/books",
        json={"title": "API Design Patterns", "author": "J.J. Geewax"},
    )
    assert created.status_code == 201
    book_id = created.get_json()["id"]

    deleted = client.delete(f"/books/{book_id}")
    assert deleted.status_code == 204

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404
    assert response.is_json
    assert response.get_json()["code"] == "NOT_FOUND"
