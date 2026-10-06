from flask import Flask, jsonify, request

app = Flask(__name__)

orders = [
    {"id": 1, "customer_id": 101, "status": "paid", "total": 100},
    {"id": 2, "customer_id": 102, "status": "pending", "total": 200},
    {"id": 3, "customer_id": 101, "status": "paid", "total": 300},
    {"id": 4, "customer_id": 103, "status": "cancelled", "total": 150},
    {"id": 5, "customer_id": 102, "status": "paid", "total": 250},
    {"id": 6, "customer_id": 101, "status": "pending", "total": 350},
]


@app.route("/orders", methods=["GET"])
def get_orders():
    result = orders.copy()

    status = request.args.get("status")
    if status:
        result = [o for o in result if o["status"] == status]

    customer_id = request.args.get("customer_id")
    if customer_id:
        result = [
            o for o in result
            if o["customer_id"] == int(customer_id)
        ]

    sort = request.args.get("sort")
    if sort:
        reverse = sort.startswith("-")
        field = sort.lstrip("-")

        if field in ["id", "customer_id", "status", "total"]:
            result.sort(
                key=lambda o: o[field],
                reverse=reverse
            )

    cursor = request.args.get("cursor")

    if cursor:
        try:
            cursor = int(cursor)
        except ValueError:
            return jsonify({
                "error": "Invalid cursor"
            }), 400

        result = [o for o in result if o["id"] > cursor]

    limit = int(request.args.get("limit", 3))
    result = result[:limit]

    next_cursor = None

    if result:
        next_cursor = result[-1]["id"]

    fields = request.args.get("fields")

    if fields:
        fields = fields.split(",")

        result = [
            {key: o[key] for key in fields if key in o}
            for o in result
        ]

    return jsonify({
        "data": result,
        "next_cursor": next_cursor
    })


if __name__ == "__main__":
    app.run(debug=True)