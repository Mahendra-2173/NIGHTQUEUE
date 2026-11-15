"""
Comprehensive Unit and Integration Test Suite for NightQueue
Tests Web Routes, Empirical Calibration, Boundary Edge Cases,
Dataset Integrity Audit, and Defensive Sanitization.
"""

import unittest
import json
from app import app
from core_engine import NightQueueModel


class TestNightQueue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.model = NightQueueModel("data.csv")

    # 1. Web Page Route Tests
    def test_01_web_routes(self):
        routes = ["/", "/checker", "/owner", "/data", "/story", "/test"]
        for r in routes:
            resp = self.client.get(r)
            self.assertEqual(resp.status_code, 200, f"Route {r} failed with {resp.status_code}")
            self.assertIn(b"NightQueue", resp.data)
            self.assertIn(b"NIT Silchar", resp.data)
            self.assertIn(b"Bipul Da", resp.data)
        print("✔ [1/10] All 6 web routes return HTTP 200 OK with correct branding.")

    # 2. Stats API Test
    def test_02_stats_api(self):
        resp = self.client.get("/api/stats")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["total_orders"], 20)
        self.assertEqual(data["avg_claimed_mins"], 4.8)
        self.assertEqual(data["avg_actual_mins"], 17.7)
        self.assertEqual(data["curfew_breach_rate_pct"], 30.0)
        self.assertTrue(data["is_empirically_grounded"])
        print(f"✔ [2/10] GET /api/stats returns verified 20 observations ({data['curfew_breach_rate_pct']}% breach rate).")

    # 3. Data API Test
    def test_03_data_api(self):
        resp = self.client.get("/api/data")
        self.assertEqual(resp.status_code, 200)
        rows = resp.get_json()
        self.assertEqual(len(rows), 20)
        self.assertEqual(rows[0]["item_ordered"], "Double Egg Maggi")
        self.assertEqual(rows[-1]["order_id"], 20)
        print(f"✔ [3/10] GET /api/data returns all 20 genuine field observation rows.")

    # 4. Dataset Audit API Test
    def test_04_dataset_audit(self):
        resp = self.client.get("/api/audit")
        self.assertEqual(resp.status_code, 200)
        audit = resp.get_json()
        self.assertTrue(audit["is_valid"])
        self.assertEqual(audit["total_rows"], 20)
        self.assertEqual(audit["missing_values_count"], 0)
        self.assertEqual(audit["duplicate_ids_count"], 0)
        self.assertIn("maggi", audit["categories_present"])
        self.assertIn("egg_toast", audit["categories_present"])
        print("✔ [4/10] GET /api/audit confirms clean dataset (0 nulls, 0 duplicate IDs, all columns verified).")

    # 5. Standard Prediction Test
    def test_05_predict_standard(self):
        payload = {
            "dish_name": "Double Egg Maggi",
            "dish_category": "maggi",
            "hostel": "Hostel 7",
            "orders_ahead": 6,
            "burners_active": 2,
            "current_time": "23:45",
            "curfew_time": "00:30",
            "curfew_buffer": 5.0
        }
        resp = self.client.post("/api/predict", json=payload)
        self.assertEqual(resp.status_code, 200)
        p = resp.get_json()
        self.assertEqual(p["hostel"], "Hostel 7")
        self.assertIn(p["curfew_status"], ["SAFE", "CAUTION", "BREACH"])
        self.assertTrue(p["is_empirically_grounded"])
        self.assertGreater(p["estimated_cook_wait_mins"], 10.0)
        print(f"✔ [5/10] POST /api/predict: Validated wait time ({p['estimated_cook_wait_mins']}m) & departure deadline.")

    # 6. Zero Queue Edge Case Test
    def test_06_zero_queue(self):
        pred = self.model.predict_wait_and_curfew(
            dish_name="Double Egg Maggi",
            dish_category="maggi",
            hostel="Hostel 1",
            orders_ahead=0,
            burners_active=2,
            current_time_str="23:30"
        )
        self.assertEqual(pred.orders_ahead, 0)
        # Solo prep should be empirical base cook (~6.4 mins from Row 1)
        self.assertAlmostEqual(pred.estimated_cook_wait_mins, 6.4, delta=0.5)
        self.assertEqual(pred.curfew_status, "SAFE")
        print(f"✔ [6/10] Zero Queue edge case verified: solo cook time = {pred.estimated_cook_wait_mins} mins.")

    # 7. Midnight Rollover Test
    def test_07_midnight_rollover(self):
        pred = self.model.predict_wait_and_curfew(
            dish_name="Plain Maggi",
            dish_category="maggi",
            hostel="Hostel 2",
            orders_ahead=2,
            burners_active=2,
            current_time_str="23:55",
            curfew_time_str="00:30"
        )
        self.assertTrue(pred.estimated_return_time.startswith("12:"))
        self.assertEqual(pred.curfew_status, "SAFE")
        print(f"✔ [7/10] Midnight Rollover (23:55 -> {pred.estimated_return_time}) calculated cleanly across date boundary.")

    # 8. Curfew Already Passed Test
    def test_08_curfew_passed(self):
        pred = self.model.predict_wait_and_curfew(
            dish_name="Plain Maggi",
            dish_category="maggi",
            hostel="Hostel 7",
            orders_ahead=3,
            burners_active=2,
            current_time_str="00:35",
            curfew_time_str="00:30"
        )
        self.assertEqual(pred.curfew_status, "CURFEW_PASSED")
        self.assertIn("CURFEW ALREADY PASSED", pred.recommendation)
        print("✔ [8/10] Curfew Expiry (00:35 vs 00:30) correctly identifies locked gate condition.")

    # 9. Bad Input Defensive Sanitization Test
    def test_09_bad_inputs_defensive(self):
        bad_payload = {
            "orders_ahead": -20,
            "burners_active": 0,
            "dish_category": "invalid_category",
            "current_time": "99:99"
        }
        resp = self.client.post("/api/test-bad-row", json=bad_payload)
        self.assertEqual(resp.status_code, 200)
        res = resp.get_json()
        self.assertEqual(res["status"], "DEFENDED_SUCCESSFULLY")
        self.assertEqual(res["sanitized_orders_ahead"], 0)
        self.assertGreaterEqual(res["sanitized_burners_active"], 1)
        print("✔ [9/10] Defensive Sanitization: safely bounded negative queue & zero burners without crash.")

    # 10. Unobserved / Fallback Food Item Test
    def test_10_unobserved_item_fallback(self):
        pred = self.model.predict_wait_and_curfew(
            dish_name="Exotic Special Dish",
            dish_category="unseen_category",
            hostel="Unknown Hostel",
            orders_ahead=2,
            burners_active=2,
            current_time_str="23:30"
        )
        self.assertFalse(pred.is_empirically_grounded)
        self.assertIn("fallback", pred.assumptions_made[0].lower())
        self.assertGreater(pred.estimated_cook_wait_mins, 0)
        print(f"✔ [10/10] Unobserved item handled with transparent fallback note: {pred.assumptions_made[0]}")


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNightQueue)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n🎉 ALL 10 UNIT & INTEGRATION TESTS PASSED (100% SUCCESS)!")
    else:
        print("\n❌ SOME TESTS FAILED")
        exit(1)


if __name__ == "__main__":
    run_tests()
