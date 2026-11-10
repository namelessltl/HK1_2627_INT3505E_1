
from flask import Blueprint, abort, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload, joinedload

from extensions import db
from models import Order, OrderItem, Product
from api.schemas import OrderIn, OrderItemIn, OrderOut

orders_bp = Blueprint(
    "orders", __name__, url_prefix="/api/v1/orders"
)


def order_query():
    return db.select(Order).options(
        selectinload(Order.items).joinedload(OrderItem.product)
    )


def add_item(order, data):
    product_id = data["product_id"]
    qty = data["qty"]

    # Không cho 1 Product xuất hiện hai lần trong cùng Order
    if any(item.product_id == product_id for item in order.items):
        abort(409, description="product already in order")

    product = db.session.scalar(
        db.select(Product).where(
            Product.id == product_id,
            Product.archived.is_(False)
        ).with_for_update()
    )

    if product is None:
        abort(404, description="product not found")

    if product.qty_in_stock < qty:
        abort(409, description="not enough stock")

    product.qty_in_stock -= qty
    order.items.append(OrderItem(product=product, qty=qty))


# POST /api/v1/orders
@orders_bp.post("")
def create_order():
    data = OrderIn().load(request.get_json(silent=True) or {})

    ids = [item["product_id"] for item in data["items"]]
    if len(ids) != len(set(ids)):
        abort(422, description="duplicate product_id")

    order = Order()
    db.session.add(order)

    try:
        for item in data["items"]:
            add_item(order, item)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return OrderOut().dump(order), 201


# GET /api/v1/orders
@orders_bp.get("")
def list_orders():
    orders = db.session.execute(
        order_query().order_by(Order.id)
    ).scalars().all()

    return {
        "items": OrderOut(many=True).dump(orders)
    }, 200


# GET /api/v1/orders/1
@orders_bp.get("/<int:id>")
def get_order(id):
    order = db.session.scalar(
        order_query().where(Order.id == id)
    )

    if order is None:
        abort(404, description="order not found")

    return OrderOut().dump(order), 200


# POST /api/v1/orders/1/items
@orders_bp.post("/<int:id>/items")
def add_order_item(id):
    data = OrderItemIn().load(
        request.get_json(silent=True) or {}
    )

    order = db.session.scalar(
        order_query().where(Order.id == id)
    )

    if order is None:
        abort(404, description="order not found")

    try:
        add_item(order, data)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, description="product already in order")
    except Exception:
        db.session.rollback()
        raise

    return OrderOut().dump(order), 201
