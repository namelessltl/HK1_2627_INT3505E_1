from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

posts = [
    {
        "id": 1,
        "title": "First post",
        "content": "Hello World",
        "author_id": 1
    },
    {
        "id": 2,
        "title": "REST API",
        "content": "Learning REST API",
        "author_id": 2
    }
]


@app.route("/api/v1/posts", methods=["GET"])
def get_posts():
    return jsonify(posts), 200


@app.route("/api/v1/posts", methods=["POST"])
def create_post():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if "title" not in data or "content" not in data:
        return jsonify({
            "error": "title and content are required"
        }), 400

    new_post = {
        "id": len(posts) + 1,
        "title": data["title"],
        "content": data["content"],
        "author_id": data.get("author_id")
    }

    posts.append(new_post)

    response = jsonify(new_post)
    response.status_code = 201

    response.headers["Location"] = url_for(
        "get_post",
        post_id=new_post["id"],
        _external=True
    )

    return response


@app.route("/api/v1/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    for post in posts:
        if post["id"] == post_id:
            return jsonify(post), 200

    return jsonify({
        "error": "Post not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)