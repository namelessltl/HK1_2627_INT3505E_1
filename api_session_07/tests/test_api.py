from sqlalchemy import event

from extensions import db
from models import Product, Order, OrderItem


def test_post_order(client, app):
    # Tạo sản phẩm mẫu
    with app.app_context():
        p = Product(
            sku="SP001",
            name="Ban phim",
            price_cents=250000,
            qty_in_stock=10
        )
        db.session.add(p)
        db.session.commit()
        product_id = p.id

    # Gửi POST tạo đơn hàng
    response = client.post("/api/v1/orders", json={
        "items": [
            {"product_id": product_id, "qty": 2}
        ]
    })

    # Kiểm tra kết quả
    assert response.status_code == 201
    assert len(response.json["items"]) == 1
    assert response.json["items"][0]["qty"] == 2

    # Kiểm tra tồn kho còn 8
    with app.app_context():
        p = db.session.get(Product, product_id)
        assert p.qty_in_stock == 8


def test_get_orders_eager_loading(client, app):
    # Tạo 5 đơn hàng, mỗi đơn có 1 sản phẩm
    with app.app_context():
        for i in range(5):
            p = Product(
                sku=f"SP{i + 100}",
                name=f"Product {i}",
                price_cents=10000,
                qty_in_stock=10
            )

            order = Order()
            order.items.append(OrderItem(product=p, qty=1))
            db.session.add(order)

        db.session.commit()

        # Xóa cache session để không che giấu N+1
        db.session.remove()

        queries = []

        # Ghi lại các câu SELECT
        def count_query(
            conn, cursor, statement,
            parameters, context, executemany
        ):
            if statement.strip().upper().startswith("SELECT"):
                queries.append(statement)

        event.listen(
            db.engine,
            "before_cursor_execute",
            count_query
        )

        try:
            response = client.get("/api/v1/orders")
        finally:
            event.remove(
                db.engine,
                "before_cursor_execute",
                count_query
            )

    # Kiểm tra API trả đủ 5 đơn hàng
    assert response.status_code == 200
    assert len(response.json["items"]) == 5

    # Kiểm tra dữ liệu Product đã được tải
    assert response.json["items"][0]["items"][0]["product"]["sku"]

    # Eager loading: chỉ cần tối đa 2 SELECT
    assert len(queries) <= 2, (
        f"Phat hien N+1: {len(queries)} SELECT"
    )
