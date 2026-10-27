from .client import call

BASE = "https://api.frankfurter.app"


def _res(name, ok, out, details=""):
    return {
        "name": name,
        "status": "PASS" if ok else "FAIL",
        "latency_ms": out["latency_ms"],
        "http_status": out["status"],
        "details": out["error"] or details,
    }


def test_status_200():
    out = call(f"{BASE}/latest", {"from": "EUR"})
    return _res("GET /latest -> 200", out["status"] == 200, out,
                f"status={out['status']}")


def test_content_type_json():
    out = call(f"{BASE}/latest", {"from": "EUR"})
    ct = out["response"].headers.get("Content-Type", "") if out["response"] else ""
    return _res("Content-Type JSON", "application/json" in ct, out, ct)


def test_required_fields():
    out = call(f"{BASE}/latest", {"from": "EUR"})
    try:
        data = out["response"].json()
        missing = [k for k in ("base", "date", "rates") if k not in data]
        return _res("Champs obligatoires", not missing, out,
                    f"manquants={missing}" if missing else "")
    except Exception as e:
        return _res("Champs obligatoires", False, out, f"JSON invalide: {e}")


def test_types():
    out = call(f"{BASE}/latest", {"from": "EUR"})
    try:
        d = out["response"].json()
        ok = (isinstance(d["base"], str) and isinstance(d["date"], str)
              and isinstance(d["rates"], dict)
              and all(isinstance(v, (int, float)) for v in d["rates"].values()))
        return _res("Types des champs", ok, out)
    except Exception as e:
        return _res("Types des champs", False, out, str(e))


def test_base_is_eur():
    out = call(f"{BASE}/latest", {"from": "EUR"})
    try:
        base = out["response"].json().get("base")
        return _res("base == EUR", base == "EUR", out, f"base={base}")
    except Exception as e:
        return _res("base == EUR", False, out, str(e))


def test_filter_to_usd():
    out = call(f"{BASE}/latest", {"from": "EUR", "to": "USD"})
    try:
        rates = out["response"].json().get("rates", {})
        return _res("Filtre to=USD", list(rates.keys()) == ["USD"], out,
                    f"clés={list(rates.keys())}")
    except Exception as e:
        return _res("Filtre to=USD", False, out, str(e))


def test_invalid_currency():
    out = call(f"{BASE}/latest", {"from": "XXX"})
    return _res("Devise invalide -> 4xx", out["status"] in (400, 404, 422), out,
                f"status={out['status']}")


def test_latency_under_2s():
    out = call(f"{BASE}/latest", {"from": "EUR"})
    return _res("Latence < 2000 ms", out["latency_ms"] < 2000, out,
                f"{out['latency_ms']} ms")


ALL_TESTS = [
    test_status_200, test_content_type_json, test_required_fields, test_types,
    test_base_is_eur, test_filter_to_usd, test_invalid_currency,
    test_latency_under_2s,
]
