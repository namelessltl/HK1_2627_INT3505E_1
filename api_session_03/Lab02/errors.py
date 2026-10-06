import uuid

from flask import jsonify, request


ERROR_BASE = "https://api.example.com/probs"


class ApiProblem(Exception):
    def __init__(
        self,
        status,
        title,
        detail=None,
        type_path=None,
        **extra
    ):
        super().__init__(title)

        self.status = status
        self.title = title
        self.detail = detail
        self.type_path = type_path
        self.extra = extra


def problem(status, title, detail=None, type_path=None, **extra):
    body = {
        "type": (
            f"{ERROR_BASE}/{type_path}"
            if type_path
            else "about:blank"
        ),
        "title": title,
        "status": status,
        "instance": request.path,
        "trace_id": str(uuid.uuid4()),
    }

    if detail:
        body["detail"] = detail

    body.update(extra)

    response = jsonify(body)

    response.status_code = status
    response.headers["Content-Type"] = "application/problem+json"

    return response