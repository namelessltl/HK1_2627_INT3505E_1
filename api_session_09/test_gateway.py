
import pytest
import gateway
from app import app


@pytest.fixture
def client(monkeypatch):
    app.config["TESTING"] = True
    monkeypatch.setattr(gateway, "V2_PERCENT", 5)
    return app.test_client()


def post_order(client, account_id, headers=None):
    return client.post(
        "/orders",
        json={"account_id": account_id},
        headers=headers or {}
    )


def test_beta_cohort(client):
    response = post_order(
        client, "any",
        {"X-Cohort": "beta"}
    )
    assert response.status_code == 201
    assert response.headers["X-Order-Handler"] == "v2"


def test_allowlist(client):
    response = post_order(client, "acct_42")
    assert response.status_code == 201
    assert response.headers["X-Order-Handler"] == "v2"


def test_bucket_v1(client):
    response = post_order(client, "regular_1")
    assert response.status_code == 200
    assert response.headers["X-Order-Handler"] == "v1"


def test_bucket_v2(client):
    response = post_order(client, "acct_normal")
    assert response.status_code == 201
    assert response.headers["X-Order-Handler"] == "v2"


def test_rollout_100(client, monkeypatch):
    monkeypatch.setattr(gateway, "V2_PERCENT", 100)

    response = post_order(client, "regular_1")
    assert response.status_code == 201
    assert response.headers["X-Order-Handler"] == "v2"
