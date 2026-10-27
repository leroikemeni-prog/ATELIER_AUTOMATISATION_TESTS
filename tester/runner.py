import math
from datetime import datetime
from zoneinfo import ZoneInfo
from .tests import ALL_TESTS


def _p95(values):
    if not values:
        return 0
    s = sorted(values)
    return s[math.ceil(0.95 * len(s)) - 1]


def run_all():
    tests = [t() for t in ALL_TESTS]
    total = len(tests)
    passed = sum(1 for t in tests if t["status"] == "PASS")
    failed = total - passed
    lats = [t["latency_ms"] for t in tests]
    available = sum(1 for t in tests
                    if t["http_status"] is not None and t["http_status"] < 500)

    return {
        "api": "Frankfurter",
        "timestamp": datetime.now(ZoneInfo("Europe/Paris")).isoformat(timespec="seconds"),
        "summary": {
            "passed": passed,
            "failed": failed,
            "error_rate": round(failed / total, 3),
            "availability": round(available / total, 3),
            "latency_ms_avg": round(sum(lats) / total),
            "latency_ms_p95": _p95(lats),
        },
        "tests": tests,
    }
