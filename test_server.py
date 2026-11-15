"""
Comprehensive 21-Point Automated Test Suite for NightQueue
Tests Backend Compatibility, Data Loading, Item Statistics, Missing/Invalid Data,
Boundary Scenarios, Date-Aware Calculations, Input Validations, Flask Endpoints, and Integration.
"""

import unittest
import tempfile
import os
import json
from app import app
from core_engine import NightQueueModel


class TestNightQueueComprehensive21(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.model = NightQueueModel("data.csv")

    # 1. CSV Loading
    def test_01_csv_loading(self):
        rep = self.model.validation_report
        self.assertTrue(rep.is_valid)
        self.assertEqual(rep.total_rows_read, 20)
        self.assertEqual(rep.valid_rows_count, 20)
        self.assertEqual(rep.excluded_rows_count, 0)
        self.assertEqual(rep.duplicate_ids_count, 0)
        self.assertEqual(rep.missing_values_count, 0)
        print("✔ [1/21] CSV loading verified: 20 genuine rows loaded without errors.")

    # 2. Average calculation
    def test_02_average_calculation(self):
        stats = self.model.get_summary_stats()
        self.assertAlmostEqual(stats["avg_actual_mins"], 17.7, places=1)
        self.assertAlmostEqual(stats["avg_claimed_mins"], 4.8, places=1)
        item_stats = self.model.get_item_statistics()
        self.assertAlmostEqual(item_stats["Plain Maggi"]["mean_actual_mins"], 17.68, places=1)
        self.assertAlmostEqual(item_stats["Double Egg Maggi"]["mean_actual_mins"], 18.57, places=1)
        print("✔ [2/21] Average calculation verified: overall mean = 17.7m, item means verified.")

    # 3. Median calculation
    def test_03_median_calculation(self):
        item_stats = self.model.get_item_statistics()
        self.assertEqual(item_stats["Plain Maggi"]["median_actual_mins"], 19.9)
        self.assertEqual(item_stats["Bun Omelette"]["median_actual_mins"], 23.95)
        self.assertEqual(item_stats["Egg Toast"]["median_actual_mins"], 20.8)
        self.assertEqual(item_stats["Double Egg Maggi"]["median_actual_mins"], 20.35)
        print("✔ [3/21] Median calculation verified: robust median baselines derived per food item.")

    # 4. Food-item-wise statistics
    def test_04_food_item_wise_statistics(self):
        item_stats = self.model.get_item_statistics()
        self.assertGreaterEqual(len(item_stats), 6)
        for name, s in item_stats.items():
            self.assertGreater(s["count"], 0)
            self.assertGreater(s["min_actual_mins"], 0)
            self.assertGreaterEqual(s["max_actual_mins"], s["min_actual_mins"])
            self.assertGreater(s["base_prep_estimate_mins"], 0)
        print(f"✔ [4/21] Food-item-wise statistics verified across all {len(item_stats)} menu items.")

    # 5. Missing values handling
    def test_05_missing_values(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(
                "order_id,timestamp,item_ordered,dish_category,queue_ahead,burners_active,claimed_wait_mins,actual_wait_mins,price_inr,hostel_origin,curfew_breach,notes\n"
                "1,23:25:10,Plain Maggi,maggi,0,2,5,6.4,35,Hostel 6,No,Valid row\n"
                "2,23:26:35,Plain Maggi,maggi,1,2,5,,35,Hostel 7,No,Missing actual wait\n"
            )
            temp_path = f.name
        try:
            m = NightQueueModel(temp_path)
            rep = m.validation_report
            self.assertEqual(rep.excluded_rows_count, 1)
            self.assertEqual(rep.valid_rows_count, 1)
            self.assertIn("missing", rep.excluded_records_details[0]["reason"].lower())
            print("✔ [5/21] Missing values safely handled: invalid record excluded and logged.")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # 6. Invalid values handling
    def test_06_invalid_values(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(
                "order_id,timestamp,item_ordered,dish_category,queue_ahead,burners_active,claimed_wait_mins,actual_wait_mins,price_inr,hostel_origin,curfew_breach,notes\n"
                "1,23:25:10,Plain Maggi,maggi,0,2,5,6.4,35,Hostel 6,No,Valid row\n"
                "2,23:26:35,Plain Maggi,maggi,1,2,5,NOT_A_NUMBER,35,Hostel 7,No,Corrupt value\n"
            )
            temp_path = f.name
        try:
            m = NightQueueModel(temp_path)
            rep = m.validation_report
            self.assertEqual(rep.excluded_rows_count, 1)
            self.assertIn("non-numeric", rep.excluded_records_details[0]["reason"].lower())
            print("✔ [6/21] Invalid values handled: non-numeric string safely excluded.")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # 7. Empty dataset handling
    def test_07_empty_dataset(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("order_id,timestamp,item_ordered,dish_category,queue_ahead,burners_active,claimed_wait_mins,actual_wait_mins,price_inr,hostel_origin,curfew_breach,notes\n")
            temp_path = f.name
        try:
            m = NightQueueModel(temp_path)
            self.assertFalse(m.has_sufficient_data)
            pred = m.predict_wait_and_curfew("Plain Maggi", "maggi", "Hostel 1", 2, 2, "23:45", "00:30")
            self.assertGreater(pred.historical_prep_mins, 0)
            self.assertTrue(any("fallback" in a.lower() for a in pred.assumptions_made))
            print("✔ [7/21] Empty dataset handled gracefully: fallback constants activated.")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # 8. Negative preparation times rejection
    def test_08_negative_prep_times(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(
                "order_id,timestamp,item_ordered,dish_category,queue_ahead,burners_active,claimed_wait_mins,actual_wait_mins,price_inr,hostel_origin,curfew_breach,notes\n"
                "1,23:25:10,Plain Maggi,maggi,0,2,5,-15.0,35,Hostel 6,No,Negative wait\n"
            )
            temp_path = f.name
        try:
            m = NightQueueModel(temp_path)
            rep = m.validation_report
            self.assertEqual(rep.excluded_rows_count, 1)
            self.assertIn("non-positive", rep.excluded_records_details[0]["reason"].lower())
            print("✔ [8/21] Negative preparation times rejected and logged.")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # 9. Zero pending orders
    def test_09_zero_pending_orders(self):
        pred = self.model.predict_wait_and_curfew(
            dish_name="Double Egg Maggi",
            dish_category="maggi",
            hostel="Hostel 1",
            orders_ahead=0,
            burners_active=2,
            current_time_str="23:30",
            curfew_time_str="00:30"
        )
        self.assertEqual(pred.orders_ahead, 0)
        self.assertEqual(pred.queue_wait_mins, 0.0)
        self.assertAlmostEqual(pred.historical_prep_mins, 6.4, delta=0.5)
        self.assertEqual(pred.estimated_cook_wait_mins, pred.historical_prep_mins)
        print("✔ [9/21] Zero pending orders verified: queue wait is exactly 0.0m.")

    # 10. Multiple pending orders
    def test_10_multiple_pending_orders(self):
        pred_low = self.model.predict_wait_and_curfew("Plain Maggi", "maggi", "Hostel 7", 2, 2, "23:45", "00:30")
        pred_high = self.model.predict_wait_and_curfew("Plain Maggi", "maggi", "Hostel 7", 8, 2, "23:45", "00:30")
        self.assertGreater(pred_high.queue_wait_mins, pred_low.queue_wait_mins)
        self.assertGreater(pred_high.total_trip_mins, pred_low.total_trip_mins)
        print(f"✔ [10/21] Multiple pending orders verified: queue wait scales from {pred_low.queue_wait_mins}m to {pred_high.queue_wait_mins}m.")

    # 11. Midnight transition
    def test_11_midnight_transition(self):
        pred = self.model.predict_wait_and_curfew("Plain Maggi", "maggi", "Hostel 1", 2, 2, "23:55", "00:30")
        self.assertTrue(pred.estimated_return_time.startswith("12:"))
        self.assertIn("AM", pred.estimated_return_time)
        self.assertEqual(pred.curfew_status, "SAFE")
        print(f"✔ [11/21] Midnight transition verified: placed 23:55 arrives {pred.estimated_return_time}.")

    # 12. Curfew already passed
    def test_12_curfew_already_passed(self):
        pred = self.model.predict_wait_and_curfew("Plain Maggi", "maggi", "Hostel 7", 2, 2, "00:45", "00:30")
        self.assertEqual(pred.curfew_status, "CURFEW ALREADY PASSED")
        self.assertIn("ALREADY PASSED", pred.recommendation)
        print("✔ [12/21] Curfew already passed correctly detects post-midnight gate lock.")

    # 13. Arrival exactly at curfew
    def test_13_arrival_at_curfew(self):
        pred = self.model.predict_wait_and_curfew("Bun Omelette", "egg_toast", "Hostel 7", 1, 2, "00:00", "00:30")
        self.assertIn(pred.curfew_status, ["WARNING", "LIKELY TO MISS CURFEW"])
        print(f"✔ [13/21] Arrival near curfew verified: margin={pred.curfew_margin_mins}m -> Status={pred.curfew_status}.")

    # 14. Insufficient historical data
    def test_14_insufficient_historical_data(self):
        pred = self.model.predict_wait_and_curfew("Exotic Special Dish", "unseen_cat", "Unknown Hostel", 2, 2, "23:30", "00:30")
        self.assertFalse(pred.is_empirically_grounded)
        self.assertTrue(any("fallback" in a.lower() for a in pred.assumptions_made))
        print("✔ [14/21] Insufficient historical data handled with transparent fallback note.")

    # 15. Invalid user inputs
    def test_15_invalid_user_inputs(self):
        _, warnings, params = self.model.validate_inputs(
            dish_name="",
            dish_category=None,
            hostel="Invalid Hostel XYZ",
            orders_ahead=-10,
            burners_active=0,
            current_time_str="99:99",
            curfew_time_str="invalid_curfew"
        )
        self.assertEqual(params["orders_ahead"], 0)
        self.assertEqual(params["burners_active"], 1)
        self.assertEqual(params["hostel"], "Hostel 7")
        self.assertEqual(params["current_time"], "23:45")
        self.assertEqual(params["curfew_time"], "00:30")
        self.assertGreater(len(warnings), 0)
        print(f"✔ [15/21] Invalid user inputs safely sanitized ({len(warnings)} warnings recorded).")

    # 16. Prediction uncertainty calculation
    def test_16_uncertainty_calculation(self):
        pred = self.model.predict_wait_and_curfew("Double Egg Maggi", "maggi", "Hostel 7", 5, 2, "23:45", "00:30")
        self.assertGreater(pred.uncertainty_buffer_mins, 0.0)
        self.assertIn("–", pred.expected_range)
        self.assertIn("±", pred.confidence_interval)
        print(f"✔ [16/21] Prediction uncertainty buffer verified: ±{pred.uncertainty_buffer_mins}m ({pred.expected_range}).")

    # 17. Correct SAFE classification
    def test_17_safe_classification(self):
        pred = self.model.predict_wait_and_curfew("Plain Maggi", "maggi", "Hostel 1", 0, 2, "23:20", "00:30")
        self.assertEqual(pred.curfew_status, "SAFE")
        self.assertGreater(pred.curfew_margin_mins, 5.0)
        print(f"✔ [17/21] Correct SAFE classification verified (Margin: +{pred.curfew_margin_mins}m).")

    # 18. Correct WARNING classification
    def test_18_warning_classification(self):
        pred = self.model.predict_wait_and_curfew("Plain Maggi", "maggi", "Hostel 1", 1, 2, "00:08", "00:30")
        self.assertEqual(pred.curfew_status, "WARNING")
        self.assertLessEqual(pred.curfew_margin_mins, 5.0)
        self.assertGreaterEqual(pred.curfew_margin_mins, 0.0)
        print(f"✔ [18/21] Correct WARNING classification verified (Margin: +{pred.curfew_margin_mins}m).")

    # 19. Correct LIKELY TO MISS CURFEW classification
    def test_19_likely_to_miss_curfew_classification(self):
        pred = self.model.predict_wait_and_curfew("Double Egg Maggi", "maggi", "Hostel 8", 10, 2, "23:55", "00:30")
        self.assertEqual(pred.curfew_status, "LIKELY TO MISS CURFEW")
        self.assertLess(pred.curfew_margin_mins, 0.0)
        print(f"✔ [19/21] Correct LIKELY TO MISS CURFEW verified (Late by {abs(pred.curfew_margin_mins)}m).")

    # 20. Flask endpoint responses
    def test_20_flask_endpoint_responses(self):
        endpoints = [
            ("/", 200),
            ("/checker", 200),
            ("/data", 200),
            ("/story", 200),
            ("/test", 200),
            ("/api/stats", 200),
            ("/api/data", 200),
            ("/api/audit", 200),
            ("/api/item-stats", 200),
        ]
        for url, expected_code in endpoints:
            r = self.client.get(url)
            self.assertEqual(r.status_code, expected_code, f"Endpoint {url} failed with {r.status_code}")
        print(f"✔ [20/21] Flask endpoints verified: all {len(endpoints)} routes return HTTP 200 OK.")

    # 21. Frontend-backend integration
    def test_21_frontend_backend_integration(self):
        payload = {
            "dish_name": "Bun Omelette",
            "dish_category": "egg_toast",
            "hostel": "Hostel 7",
            "orders_ahead": 4,
            "burners_active": 2,
            "current_time": "23:45",
            "curfew_time": "00:30",
            "curfew_buffer": 5.0
        }
        resp = self.client.post("/api/predict", json=payload)
        self.assertEqual(resp.status_code, 200)
        d = resp.get_json()

        # Check all fields required by frontend JavaScript
        frontend_required_fields = [
            "walk_one_way_mins", "historical_prep_mins", "queue_wait_mins",
            "estimated_cook_wait_mins", "estimated_return_time", "departure_deadline",
            "curfew_time", "uncertainty_buffer_mins", "curfew_status",
            "curfew_margin_mins", "recommendation", "calculation_explanation",
            "historical_data_used", "expected_range", "validation_warnings",
            "is_empirically_grounded"
        ]
        for field_name in frontend_required_fields:
            self.assertIn(field_name, d, f"Missing frontend-required field: {field_name}")

        # Check mathematical consistency
        expected_cook = round(d["historical_prep_mins"] + d["queue_wait_mins"], 1)
        self.assertAlmostEqual(d["estimated_cook_wait_mins"], expected_cook, delta=0.2)
        expected_trip = round((d["walk_one_way_mins"] * 2) + d["estimated_cook_wait_mins"], 1)
        self.assertAlmostEqual(d["total_trip_mins"], expected_trip, delta=0.2)
        print("✔ [21/21] Frontend-backend integration verified: response schema & mathematical consistency confirmed.")


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNightQueueComprehensive21)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n🎉 ALL 21 COMPREHENSIVE TESTS PASSED WITH 100% SUCCESS!")
    else:
        print("\n❌ SOME TESTS FAILED")
        exit(1)


if __name__ == "__main__":
    run_tests()
