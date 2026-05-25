#!/usr/bin/env python3
"""Pre-demo smoke test for AMA stateful demo."""
import json
import sys
import time
import urllib.error
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:18080"
SEASONS = ["spring", "summer", "autumn", "winter"]


def req(path, method="GET", body=None, expect=(200,)):
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=20) as resp:
            raw = resp.read()
            if resp.status not in expect:
                raise AssertionError(f"{method} {path}: status {resp.status}, expected {expect}: {raw[:300]!r}")
            ctype = resp.headers.get("content-type", "")
            return raw.decode("utf-8") if "text/html" in ctype else json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        if e.code in expect:
            return json.loads(raw) if raw else {}
        raise AssertionError(f"{method} {path}: HTTP {e.code}: {raw[:500]}") from e


def assert_has(obj, key, ctx):
    if key not in obj:
        raise AssertionError(f"{ctx}: missing {key}")


checks = []

health = req("/health")
assert health["status"] == "healthy"
checks.append("health")

home = req("/")
for needle in ["startRun", "approveOrder", "completeOrder", "/api/v1/runs/", "Agent Runtime", "KPI"]:
    if needle not in home:
        raise AssertionError(f"frontend missing {needle}")
checks.append("frontend-html-and-js")

api = req("/api")
assert api["status"] == "running"
assert len(api["agents"]) == 5
checks.append("api-root")

seasons = req("/api/v1/seasons")["seasons"]
season_ids = [s.get("id", s) if isinstance(s, dict) else s for s in seasons]
if set(SEASONS) - set(season_ids):
    raise AssertionError(f"seasons missing: {set(SEASONS)-set(season_ids)}")
checks.append("season-list")

for season in SEASONS:
    scenario = req(f"/api/v1/season/{season}", method="POST")
    for key in ["decision_loop", "products", "customers", "trigger"]:
        assert_has(scenario, key, f"season {season}")
    if len(scenario["decision_loop"]) != 5:
        raise AssertionError(f"season {season}: decision loop != 5")

    run = req(f"/api/v1/runs/{season}?region=china", method="POST")
    for key in ["run_id", "scenario", "work_orders", "execution_trace", "shared_memory", "kpi_simulation", "audit_log", "fashion_launch"]:
        assert_has(run, key, f"run {season}")
    if not run["work_orders"]:
        raise AssertionError(f"run {season}: no work orders")
    if len(run["execution_trace"]) < 5:
        raise AssertionError(f"run {season}: execution trace too short")
    rid = run["run_id"]

    # Status endpoint and approve/complete state machine.
    status = req(f"/api/v1/runs/{rid}/status")
    assert status["run_id"] == rid

    pending = next((o for o in status["work_orders"] if o["status"] == "PENDING_APPROVAL"), None)
    if pending:
        conflict = req(f"/api/v1/runs/{rid}/work-orders/{pending['id']}/complete", method="POST", expect=(409,))
        if "Approve" not in conflict.get("detail", ""):
            raise AssertionError(f"run {season}: pending complete did not return approval-needed conflict")
        approved = req(f"/api/v1/runs/{rid}/work-orders/{pending['id']}/approve", method="POST")
        new_order = next(o for o in approved["work_orders"] if o["id"] == pending["id"])
        if new_order["status"] != "READY":
            raise AssertionError(f"run {season}: approve did not set READY")
        completed = req(f"/api/v1/runs/{rid}/work-orders/{pending['id']}/complete", method="POST")
        done_order = next(o for o in completed["work_orders"] if o["id"] == pending["id"])
        if done_order["status"] != "COMPLETED":
            raise AssertionError(f"run {season}: complete did not set COMPLETED")
    checks.append(f"run-{season}")

custom_payload = {
    "season": "summer",
    "sku_id": "DEMO-SKU-001",
    "product_name": "Demo Breathable Jacket",
    "current_price": 299,
    "cost": 110,
    "current_stock": 120,
    "safety_stock": 300,
    "warehouse_available": 1000,
    "baseline_daily_sales": 45,
    "app_views_24h": 12000,
    "cart_adds_24h": 860,
    "rfid_tryons_24h": 210,
    "demand_multiplier": 2.1,
    "baseline_ctr_pct": 4.8,
    "target_ctr_pct": 6.2,
    "live_empty_slots": 16,
}
custom = req("/api/v1/runs/custom?region=china", method="POST", body=custom_payload)
assert custom["scenario"]["season"] == "summer"
assert custom["fashion_launch"]["hero_sku"] == "DEMO-SKU-001"
checks.append("custom-launch")

print(json.dumps({"ok": True, "checks": checks}, ensure_ascii=False, indent=2))
