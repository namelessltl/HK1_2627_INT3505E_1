import pytest
from app import create_app
from models import Book, Category, db


@pytest.fixture
def client(tmp_path):
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(tmp_path / "lab02_test.sqlite"),
    })
    with app.app_context():
        literature = Category(name="Văn học", slug="van-hoc")
        it = Category(name="CNTT", slug="cong-nghe-thong-tin")
        db.session.add_all([literature, it])
        db.session.flush()
        for title, isbn, price, category in [
            ("Mat Biec", "isbn01", 110000, literature),
            ("Clean Code", "isbn02", 350000, it),
            ("Another Code", "isbn03", 350000, it),
            ("Python 101", "isbn04", 200000, it),
            ("Doraemon", "isbn05", 110000, literature),
            ("SQL Guide", "isbn06", 200000, it),
        ]:
            db.session.add(Book(title=title, isbn=isbn, price_vnd=price,
                                stock=5, category=category))
        db.session.commit()

    with app.test_client() as test_client:
        yield test_client

def ids(response):
    return [item["id"] for item in response.json["items"]]


def test_offset_pagination(client):
    first = client.get("/api/v1/books?strategy=offset&sort=id&limit=2&offset=0")
    assert first.status_code == 200
    assert ids(first) == [1, 2]
    assert first.json["next_offset"] == 2
    assert first.json["next_cursor"] is None
    assert first.json["has_more"] is True

    second = client.get("/api/v1/books?strategy=offset&sort=id&limit=2&offset=2")
    assert ids(second) == [3, 4]
    assert second.json["next_offset"] == 4

    last = client.get("/api/v1/books?strategy=offset&sort=id&limit=2&offset=4")
    assert ids(last) == [5, 6]
    assert last.json["next_offset"] is None
    assert last.json["has_more"] is False


def test_cursor_full_walk_tied_price(client):
    base_url = "/api/v1/books?strategy=cursor&sort=-price&limit=2"
    token = None
    found = []
    for _ in range(10):
        url = base_url if token is None else base_url + "&cursor=" + token
        response = client.get(url)
        assert response.status_code == 200
        found.extend(ids(response))
        token = response.json["next_cursor"]
        if token is None:
            assert response.json["has_more"] is False
            break
    else:
        pytest.fail("Cursor did not terminate")

    assert found == [3, 2, 6, 4, 5, 1]
    assert len(found) == len(set(found)) == 6


def test_multi_key_sort_and_tie_breaker(client):
    result = client.get("/api/v1/books?sort=-price,title&limit=100")
    assert result.status_code == 200
    assert ids(result) == [3, 2, 4, 6, 5, 1]


def test_cursor_with_multi_key_sort(client):
    url = "/api/v1/books?sort=-price,title&limit=1"
    first = client.get(url)
    second = client.get(url + "&cursor=" + first.json["next_cursor"])
    assert ids(first) == [3]
    assert ids(second) == [2]


def test_genre_filter_by_category_slug(client):
    result = client.get("/api/v1/books?genre=van-hoc&sort=-price")
    assert result.status_code == 200
    assert ids(result) == [5, 1]


def test_genre_and_category_id_filter(client):
    result = client.get("/api/v1/books?genre=van-hoc&category_id=2")
    assert result.status_code == 200
    assert ids(result) == []


def test_cursor_rejects_changed_sort_and_filter(client):
    first = client.get("/api/v1/books?sort=-price&limit=1")
    token = first.json["next_cursor"]
    assert token
    wrong_sort = client.get("/api/v1/books?sort=price&limit=1&cursor=" + token)
    wrong_genre = client.get("/api/v1/books?sort=-price&genre=van-hoc&cursor=" + token)
    assert wrong_sort.status_code == 400
    assert wrong_sort.json["error"] == "bad_cursor"
    assert wrong_genre.status_code == 400
    assert wrong_genre.json["error"] == "bad_cursor"


@pytest.mark.parametrize("qs,error", [
    ("sort=-foo", "bad_sort"),
    ("sort=-price,title,", "bad_sort"),
    ("sort=price,price", "bad_sort"),
    ("limit=0", "bad_limit"),
    ("limit=101", "bad_limit"),
    ("strategy=unknown", "bad_strategy"),
    ("strategy=offset&offset=-1", "bad_offset"),
    ("strategy=offset&offset=abc", "bad_parameter"),
    ("genre=", "bad_genre"),
    ("strategy=cursor&cursor=not-valid", "bad_cursor"),
    ("strategy=cursor&cursor=", "bad_cursor"),
    ("strategy=cursor&offset=2", "bad_offset"),
    ("strategy=offset&cursor=abc", "bad_cursor"),
])
def test_invalid_input(client, qs, error):
    response = client.get("/api/v1/books?" + qs)
    assert response.status_code == 400
    assert response.json["error"] == error


def test_post_and_get_still_work(client):
    response = client.post("/api/v1/books", json={
        "title": "New Book", "isbn": "isbn07", "price_vnd": 80000,
        "stock": 3, "category_id": 1,
    })
    assert response.status_code == 201
    assert response.json["id"] == 7
    book = client.get("/api/v1/books/7")
    assert book.status_code == 200
    assert book.json["title"] == "New Book"
