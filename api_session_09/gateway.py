
# gateway.py

import hashlib
import logging
from flask import request
from handlers import v1_create_order, v2_create_order

# Tỷ lệ request thông thường chuyển sang v2
V2_PERCENT = 5

# Cohort được ưu tiên sử dụng v2
V2_COHORTS = {"beta", "internal"}

# Tài khoản luôn sử dụng v2
V2_FORCE_ACCOUNTS = {"acct_42", "acct_99"}

log = logging.getLogger("gateway")


def route_to_v2(body):
    # 1. Ưu tiên cohort
    cohort = request.headers.get(
        "X-Cohort", ""
    ).strip().lower()

    if cohort in V2_COHORTS:
        return True

    # 2. Ưu tiên tài khoản allow-list
    acct = str(body.get("account_id", ""))

    if acct in V2_FORCE_ACCOUNTS:
        return True

    # 3. Chia theo tỷ lệ phần trăm
    if V2_PERCENT <= 0:
        return False

    if V2_PERCENT >= 100:
        return True

    h = int(
        hashlib.md5(
            acct.encode("utf-8")
        ).hexdigest(),
        16
    )

    return h % 100 < V2_PERCENT


def dispatch(body):
    if route_to_v2(body):
        log.info("Routing account to v2")
        return "v2", v2_create_order(body)

    log.info("Routing account to v1")
    return "v1", v1_create_order(body)
