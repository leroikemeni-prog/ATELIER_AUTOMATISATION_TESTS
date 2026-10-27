import time
import requests

TIMEOUT = 4  # secondes


def call(url, params=None, retries=1):
    """GET avec timeout, 1 retry max, gestion 429/5xx, mesure de latence."""
    attempt = 0
    while True:
        start = time.perf_counter()
        try:
            r = requests.get(url, params=params, timeout=TIMEOUT)
            latency = round((time.perf_counter() - start) * 1000)

            if r.status_code == 429 and attempt < retries:
                try:
                    wait = min(int(r.headers.get("Retry-After", 2)), 5)
                except ValueError:
                    wait = 2
                time.sleep(wait)
                attempt += 1
                continue

            if r.status_code >= 500 and attempt < retries:
                time.sleep(1)
                attempt += 1
                continue

            return {"response": r, "status": r.status_code,
                    "latency_ms": latency, "error": None}

        except requests.RequestException as e:
            latency = round((time.perf_counter() - start) * 1000)
            if attempt < retries:
                attempt += 1
                continue
            return {"response": None, "status": None,
                    "latency_ms": latency, "error": str(e)}
