"""
Unit and Integration Tests for NightQueue Flask App
Uses Flask's internal WSGI test client (no network sockets needed).
"""

from app import app
import json

def run_tests():
    client = app.test_client()
    
    # 1. Test Home page
    r = client.get("/")
    assert r.status_code == 200, f"Home failed: {r.status_code}"
    assert b"NightQueue" in r.data
    assert b"NIT Silchar" in r.data
    assert b"Bipul Da" in r.data
    print("✔ [1/4] GET / : 200 OK (HTML Template loaded with NIT Silchar & Bipul Da)")

    # 2. Test Stats API
    r = client.get("/api/stats")
    assert r.status_code == 200, f"Stats failed: {r.status_code}"
    stats = r.get_json()
    assert stats["total_orders"] == 20
    assert stats["avg_claimed_mins"] == 4.8
    assert stats["avg_actual_mins"] == 17.7
    print(f"✔ [2/4] GET /api/stats : 200 OK (20 orders, {stats['curfew_breach_rate_pct']}% curfew breaches)")

    # 3. Test Raw Data API
    r = client.get("/api/data")
    assert r.status_code == 200, f"Data failed: {r.status_code}"
    rows = r.get_json()
    assert len(rows) == 20
    print(f"✔ [3/4] GET /api/data : 200 OK (Loaded {len(rows)} real fieldwork records)")

    # 4. Test Predict API
    payload = {
        "dish_name": "Double Egg Maggi",
        "dish_category": "maggi",
        "hostel": "Hostel 7",
        "orders_ahead": 6,
        "burners_active": 2,
        "current_time": "23:45",
        "curfew_buffer": 5.0
    }
    r = client.post("/api/predict", json=payload)
    assert r.status_code == 200, f"Predict failed: {r.status_code}"
    pred = r.get_json()
    assert "curfew_status" in pred
    assert pred["hostel"] == "Hostel 7"
    print(f"✔ [4/4] POST /api/predict : 200 OK (Status: {pred['curfew_status']}, Cook Wait: {pred['estimated_cook_wait_mins']}m, Return: {pred['estimated_return_time']})")

    # 5. Test Bad Row Stress Defense (Call viva requirement)
    bad_payload = {"orders_ahead": -20, "burners_active": 0, "dish_category": "invalid"}
    r = client.post("/api/test-bad-row", json=bad_payload)
    assert r.status_code == 200, f"Bad row failed: {r.status_code}"
    bad_res = r.get_json()
    assert bad_res["status"] == "DEFENDED_SUCCESSFULLY"
    assert bad_res["sanitized_orders_ahead"] == 0
    assert bad_res["sanitized_burners_active"] == 1
    print(f"✔ [BONUS] POST /api/test-bad-row : 200 OK (Sanitized cleanly: {bad_res['defense_note']})")

    print("\n🎉 ALL 5 INTEGRATION SUITE TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run_tests()
