"""
Comprehensive Test Suite for NightQueue (All 19 Assignment Requirements)
Tests Data Loading, Item-wise Statistics, Median/Mean Calculations, Missing/Invalid Data,
Boundary Conditions, Midnight Arithmetic, Input Validations, and Classification Integrity.
"""

import unittest
import tempfile
import os
import pandas as pd
from app import app
from core_engine import NightQueueModel


class TestNightQueueComprehensive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.model = NightQueueModel("data.csv")

    # 1. Correct CSV Loading
    def test_01_correct_csv_loading(self):
        rep = self.model.validation_report
        self.assertTrue(rep.is_valid)
        self.assertEqual(rep.total_rows_read, 20)
        self.assertEqual(rep.valid_rows_count, 20)
        self.assertEqual(rep.excluded_rows_count, 0)
        print("✔ [1/19] Correct CSV loading verified: 20 genuine rows loaded.")

    # 2. Food-item-wise preparation-time calculation
    def test_02_food_item_wise_prep_time(self):
        item_stats = self.model.get_item_statistics()
        self.assertIn("Plain Maggi", item_stats)
        self.assertIn("Double Egg Maggi", item_stats)
        self.assertIn("Bun Omelette", item_stats)
        self.assertIn("Egg Toast", item_stats)
        for name, s in item_stats.items():
            self.assertGreater(s["count"], 0)
            self.assertGreater(s["base_prep_estimate_mins"], 0)
        print(f"✔ [2/19] Food-item-wise preparation times calculated for {len(item_stats)} items.")

    # 3. Average calculation
    def test_03_average_calculation(self):
        stats = self.model.get_summary_stats()
        self.assertAlmostEqual(stats["avg_actual_mins"], 17.7, places=1)
        self.assertAlmostEqual(stats["avg_claimed_mins"], 4.8, places=1)
        item_stats = self.model.get_item_statistics()
        self.assertAlmostEqual(item_stats["Plain Maggi"]["mean_actual_mins"], 17.68, places=1)
        print("✔ [3/19] Average calculation verified: overall mean = 17.7m, Plain Maggi mean = 17.68m.")

    # 4. Median calculation
    def test_04_median_calculation(self):
        item_stats = self.model.get_item_statistics()
        self.assertEqual(item_stats["Plain Maggi"]["median_actual_mins"], 19.9)
        self.assertEqual(item_stats["Bun Omelette"]["median_actual_mins"], 23.95)
        self.assertEqual(item_stats["Egg Toast"]["median_actual_mins"], 20.8)
        print("✔ [4/19] Median calculation verified: Plain Maggi median = 19.9m, Bun Omelette = 23.95m.")

    # 5. Missing CSV values handling
    def test_05_missing_csv_values(self):
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
            print("✔ [5/19] Missing CSV values safely handled: row excluded and logged.")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # 6. Invalid CSV values handling
    def test_06_invalid_csv_values(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(
                "order_id,timestamp,item_ordered,dish_category,queue_ahead,burners_active,claimed_wait_mins,actual_wait_mins,price_inr,hostel_origin,curfew_breach,notes\n"
                "1,23:25:10,Plain Maggi,maggi,0,2,5,6.4,35,Hostel 6,No,Valid row\n"
                "2,23:26:35,Plain Maggi,maggi,1,2,5,CORRUPT_STRING,35,Hostel 7,No,Corrupt value\n"
            )
            temp_path = f.name
        try:
            m = NightQueueModel(temp_path)
            rep = m.validation_report
            self.assertEqual(rep.excluded_rows_count, 1)
            self.assertIn("non-numeric", rep.excluded_records_details[0]["reason"].lower())
            print("✔ [6/19] Invalid CSV values handled: non-numeric string safely excluded.")
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
            print("✔ [7/19] Empty dataset handled gracefully: fallback constants activated.")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # 8. Negative preparation times rejection
    def test_08_negative_prep_times(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(
                "order_id,timestamp,item_ordered,dish_category,queue_ahead,burners_active,claimed_wait_mins,actual_wait_mins,price_inr,hostel_origin,curfew_breach,notes\n"
                "1,23:25:10,Plain Maggi,maggi,0,2,5,-10.5,35,Hostel 6,No,Negative wait\n"
            )
            temp_path = f.name
        try:
            m = NightQueueModel(temp_path)
            rep = m.validation_report
            self.assertEqual(rep.excluded_rows_count, 1)
            self.assertIn("non-positive", rep.excluded_records_details[0]["reason"].lower())
            print("✔ [8/19] Negative preparation times rejected and logged.")
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
        print("✔ [9/19] Zero pending orders verified: queue wait is exactly 0.0 mins.")

    # 10. Multiple pending orders
    def test_10_multiple_pending_orders(self):
        pred_low = self.model.predict_wait_and_curfew("Plain Maggi", "maggi", "Hostel 7", 2, 2, "23:45", "00:30")
        pred_high = self.model.predict_wait_and_curfew("Plain Maggi", "maggi", "Hostel 7", 8, 2, "23:45", "00:30")
        self.assertGreater(pred_high.queue_wait_mins, pred_low.queue_wait_mins)
        self.assertGreater(pred_high.total_trip_mins, pred_low.total_trip_mins)
        print(f"✔ [10/19] Multiple pending orders verified: queue wait scaled from {pred_low.queue_wait_mins}m to {pred_high.queue_wait_mins}m.")

    # 11. Midnight transition
    def test_11_midnight_transition(self):
        pred = self.model.predict_wait_and_curfew("Plain Maggi", "maggi", "Hostel 1", 2, 2, "23:55", "00:30")
        self.assertTrue(pred.estimated_return_time.startswith("12:"))
        self.assertIn("AM", pred.estimated_return_time)
        self.assertEqual(pred.curfew_status, "SAFE")
        print(f"✔ [11/19] Midnight transition verified: order placed 23:55 arrives {pred.estimated_return_time}.")

    # 12. Curfew already passed
    def test_12_curfew_already_passed(self):
        pred = self.model.predict_wait_and_curfew("Plain Maggi", "maggi", "Hostel 7", 2, 2, "00:45", "00:30")
        self.assertEqual(pred.curfew_status, "CURFEW ALREADY PASSED")
        self.assertIn("ALREADY PASSED", pred.recommendation)
        print("✔ [12/19] Curfew already passed correctly detects post-midnight gate lock.")

    # 13. Arrival exactly at curfew
    def test_13_arrival_at_curfew(self):
        # Current time 00:00, curfew 00:30, trip ~30 mins
        pred = self.model.predict_wait_and_curfew("Bun Omelette", "egg_toast", "Hostel 7", 1, 2, "00:00", "00:30")
        # With tight buffer (margin <= 5 mins), status must be WARNING or LIKELY TO MISS CURFEW
        self.assertIn(pred.curfew_status, ["WARNING", "LIKELY TO MISS CURFEW"])
        print(f"✔ [13/19] Arrival near/at curfew verified: margin={pred.curfew_margin_mins}m -> Status={pred.curfew_status}.")

    # 14. Insufficient historical data
    def test_14_insufficient_historical_data(self):
        pred = self.model.predict_wait_and_curfew("Exotic Unseen Dish", "unseen_cat", "Unknown Hostel", 2, 2, "23:30", "00:30")
        self.assertFalse(pred.is_empirically_grounded)
        self.assertTrue(any("fallback" in a.lower() for a in pred.assumptions_made))
        print(f"✔ [14/19] Insufficient historical data handled with transparent fallback note.")

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
        print(f"✔ [15/19] Invalid user inputs safely sanitized ({len(warnings)} warnings recorded).")

    # 16. Prediction uncertainty calculation
    def test_16_prediction_uncertainty_calculation(self):
        pred = self.model.predict_wait_and_curfew("Double Egg Maggi", "maggi", "Hostel 7", 5, 2, "23:45", "00:30")
        self.assertGreater(pred.uncertainty_buffer_mins, 0.0)
        self.assertIn("–", pred.expected_range)
        print(f"✔ [16/19] Prediction uncertainty buffer verified: ±{pred.uncertainty_buffer_mins}m ({pred.expected_range}).")

    # 17. Correct SAFE classification
    def test_17_correct_safe_classification(self):
        # 23:20, 0 queue, Hostel 1 (5 mins walk)
        pred = self.model.predict_wait_and_curfew("Plain Maggi", "maggi", "Hostel 1", 0, 2, "23:20", "00:30")
        self.assertEqual(pred.curfew_status, "SAFE")
        self.assertGreater(pred.curfew_margin_mins, 5.0)
        print(f"✔ [17/19] Correct SAFE classification verified (Margin: +{pred.curfew_margin_mins}m).")

    # 18. Correct WARNING classification
    def test_18_correct_warning_classification(self):
        # 00:08, 1 queue, Hostel 1 (5 mins walk) -> Returns ~00:26 AM (4 mins before 00:30)
        pred = self.model.predict_wait_and_curfew("Plain Maggi", "maggi", "Hostel 1", 1, 2, "00:08", "00:30")
        self.assertEqual(pred.curfew_status, "WARNING")
        self.assertLessEqual(pred.curfew_margin_mins, 5.0)
        self.assertGreaterEqual(pred.curfew_margin_mins, 0.0)
        print(f"✔ [18/19] Correct WARNING classification verified (Margin: +{pred.curfew_margin_mins}m).")

    # 19. Correct LIKELY TO MISS CURFEW classification
    def test_19_correct_likely_to_miss_curfew_classification(self):
        # 23:55, 10 queue, Hostel 8 (9 mins walk) -> Returns ~00:40 AM (Late!)
        pred = self.model.predict_wait_and_curfew("Double Egg Maggi", "maggi", "Hostel 8", 10, 2, "23:55", "00:30")
        self.assertEqual(pred.curfew_status, "LIKELY TO MISS CURFEW")
        self.assertLess(pred.curfew_margin_mins, 0.0)
        print(f"✔ [19/19] Correct LIKELY TO MISS CURFEW classification verified (Late by {abs(pred.curfew_margin_mins)}m).")


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNightQueueComprehensive)
    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n🎉 ALL 19 COMPREHENSIVE TESTS PASSED WITH 100% SUCCESS!")
    else:
        print("\n❌ SOME TESTS FAILED")
        exit(1)


if __name__ == "__main__":
    run_tests()
