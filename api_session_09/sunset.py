from datetime import datetime, timezone
from email.utils import format_datetime
from functools import wraps
from flask import request, jsonify, make_response
import logging

log = logging.getLogger("sunset")


def http_date(dt):
    return format_datetime(
        dt.astimezone(timezone.utc),
        usegmt=True
    )


def deprecate_at(sunset_date, replacement=None):
    if sunset_date.tzinfo is None:
        raise ValueError("sunset_date must have timezone")

    def wrap(fn):
        @wraps(fn)
        def inner(*a, **kw):
            now = datetime.now(timezone.utc)

            log.warning(
                "deprecated_call %s %s",
                request.path,
                request.remote_addr
            )

            # Sau sunset
            if now >= sunset_date:
                body = {
                    "error": "gone",
                    "sunset": http_date(sunset_date)
                }

                if replacement:
                    body["use_instead"] = replacement

                return jsonify(body), 410

            # Trước sunset
            result = fn(*a, **kw)
            response = make_response(result)

            response.headers["Sunset"] = http_date(sunset_date)
            response.headers["Deprecation"] = "true"

            if replacement:
                response.headers["Link"] = (
                    f'<{replacement}>; '
                    'rel="successor-version"'
                )

            return response

        return inner

    return wrap
