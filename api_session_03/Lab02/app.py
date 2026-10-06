from flask import Flask, jsonify

from errors import ApiProblem, problem


app = Flask(__name__)


users = [
    {
        "id": 1,
        "name": "An"
    },
    {
        "id": 2,
        "name": "Binh"
    }
]


@app.errorhandler(ApiProblem)
def handle_api_problem(error):
    return problem(
        status=error.status,
        title=error.title,
        detail=error.detail,
        type_path=error.type_path,
        **error.extra
    )


@app.get("/users/<int:id>")
def get_user(id):
    user = next(
        (user for user in users if user["id"] == id),
        None
    )

    if not user:
        raise ApiProblem(
            status=404,
            title="User not found",
            type_path="user-not-found",
            resource_id=id
        )

    return jsonify(user), 200


if __name__ == "__main__":
    app.run(debug=True)