
# handlers.py

def v1_create_order(body):
    return {
        "message": "Order created by v1",
        "account_id": body.get("account_id"),
        "items": body.get("items", []),
        "version": "v1"
    }


def v2_create_order(body):
    return {
        "message": "Order created by v2",
        "account_id": body.get("account_id"),
        "items": body.get("items", []),
        "status": "created",
        "version": "v2"
    }
