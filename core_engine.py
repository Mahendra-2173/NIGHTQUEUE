"""
NightQueue Core Engine: Queue Wait Time & Curfew Safety Calculator
Calculates real cooking times and curfew risks for Bipul Da's stall at Gate 1, NIT Silchar.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Optional
import os
import pandas as pd


# NIT Silchar campus walking times to Gate 1 (one-way in minutes)
NIT_SILCHAR_HOSTEL_WALK_TIMES = {
    "Hostel 1": 5.0,
    "Hostel 2": 5.0,
    "Hostel 3": 6.0,
    "Hostel 4": 6.5,
    "Hostel 5": 7.0,
    "Hostel 6": 7.5,
    "Hostel 7": 8.0,
    "Hostel 8": 9.0,
    "Hostel 9 (PG)": 11.0,
    "Girls Hostel 1": 10.0,
    "Girls Hostel 2": 10.5,
}

# Base cooking times per item category (in minutes)
BASE_COOK_TIMES = {
    "maggi": 4.5,
    "egg_toast": 6.0,
    "beverage": 2.5,
    "bakery": 3.0,
}

# Time needed to wipe and oil the pan between egg dishes and Maggi
PAN_CLEANING_PENALTY_MINS = 1.2


@dataclass
class QueuePrediction:
    item_name: str
    dish_category: str
    hostel: str
    orders_ahead: int
    burners_active: int
    vendor_promised_mins: float
    estimated_cook_wait_mins: float
    walk_one_way_mins: float
    total_trip_mins: float
    estimated_ready_time: str
    estimated_return_time: str
    curfew_time: str
    curfew_status: str  # "SAFE", "CAUTION", "BREACH"
    curfew_margin_mins: float
    recommendation: str
    empirical_error_spread_mins: float


class NightQueueModel:
    def __init__(self, data_csv_path: str = "data.csv"):
        self.data_csv_path = data_csv_path
        self.df = None
        self.load_data()

    def load_data(self) -> None:
        """Loads data.csv containing 20 real orders collected at the stall."""
        if os.path.exists(self.data_csv_path):
            try:
                self.df = pd.read_csv(self.data_csv_path)
            except Exception as e:
                print(f"[Warning] Could not read {self.data_csv_path}: {e}")
                self.df = pd.DataFrame()
        else:
            self.df = pd.DataFrame()

    def get_summary_stats(self) -> Dict[str, float]:
        """Calculates simple summary numbers from the 20 real orders."""
        if self.df is None or self.df.empty:
            return {
                "total_orders": 0,
                "avg_claimed_mins": 5.0,
                "avg_actual_mins": 18.0,
                "avg_underestimation_gap": 13.0,
                "curfew_breach_rate_pct": 35.0,
            }

        # Filter valid rows
        valid_df = self.df.dropna(subset=["claimed_wait_mins", "actual_wait_mins"]).copy()
        valid_df["claimed_wait_mins"] = pd.to_numeric(valid_df["claimed_wait_mins"], errors="coerce")
        valid_df["actual_wait_mins"] = pd.to_numeric(valid_df["actual_wait_mins"], errors="coerce")
        valid_df = valid_df[(valid_df["claimed_wait_mins"] > 0) & (valid_df["actual_wait_mins"] > 0)]

        if valid_df.empty:
            return {
                "total_orders": 0,
                "avg_claimed_mins": 5.0,
                "avg_actual_mins": 18.0,
                "avg_underestimation_gap": 13.0,
                "curfew_breach_rate_pct": 35.0,
            }

        avg_claimed = float(valid_df["claimed_wait_mins"].mean())
        avg_actual = float(valid_df["actual_wait_mins"].mean())
        breaches = valid_df[valid_df["curfew_breach"].str.strip().str.lower() == "yes"]
        breach_rate = float((len(breaches) / len(valid_df)) * 100.0)

        return {
            "total_orders": int(len(valid_df)),
            "avg_claimed_mins": round(avg_claimed, 2),
            "avg_actual_mins": round(avg_actual, 2),
            "avg_underestimation_gap": round(avg_actual - avg_claimed, 2),
            "curfew_breach_rate_pct": round(breach_rate, 1),
        }

    def predict_wait_and_curfew(
        self,
        dish_name: str,
        dish_category: str,
        hostel: str,
        orders_ahead: int,
        burners_active: int = 2,
        current_time_str: Optional[str] = None,
        curfew_time_str: str = "00:30",
        curfew_buffer_mins: float = 5.0,
    ) -> QueuePrediction:
        """
        Calculates realistic cooking wait time and whether the student will reach
        their hostel before the 12:30 AM curfew.
        """
        # Protect against negative or bad inputs
        safe_orders_ahead = max(0, int(orders_ahead))
        safe_burners = max(1, int(burners_active))
        dish_category = dish_category.lower() if dish_category else "maggi"

        base_cook = BASE_COOK_TIMES.get(dish_category, 5.0)
        walk_time = NIT_SILCHAR_HOSTEL_WALK_TIMES.get(hostel, 7.5)

        # Cooking time calculation:
        # Bipul Da splits orders across available burners.
        # Maggi can be batched together (2 in one pot), while egg dishes take individual tawa time.
        effective_batches = safe_orders_ahead / safe_burners
        if dish_category == "maggi":
            effective_batches *= 0.75

        # Pan cleaning delay happens every ~3 mixed orders
        pan_cleanings = safe_orders_ahead // 3
        cleaning_delay = pan_cleanings * PAN_CLEANING_PENALTY_MINS

        # Total estimated cooking wait
        estimated_cook_wait = (effective_batches * base_cook) + base_cook + cleaning_delay

        # Determine current clock time
        now = datetime.now()
        if current_time_str:
            try:
                parts = [int(p) for p in current_time_str.split(":")]
                now = now.replace(hour=parts[0], minute=parts[1], second=0, microsecond=0)
            except Exception:
                pass

        # Total trip = Walk to Gate 1 + Cooking wait + Walk back to hostel
        total_trip_mins = walk_time + estimated_cook_wait + walk_time

        ready_dt = now + timedelta(minutes=estimated_cook_wait)
        return_dt = now + timedelta(minutes=total_trip_mins)

        # Determine curfew time (12:30 AM)
        curfew_hour, curfew_min = [int(p) for p in curfew_time_str.split(":")]
        curfew_dt = now.replace(hour=curfew_hour, minute=curfew_min, second=0, microsecond=0)
        if curfew_dt < now:
            # If current time is 23:45 and curfew is 00:30, curfew is past midnight
            curfew_dt += timedelta(days=1)

        curfew_margin = (curfew_dt - return_dt).total_seconds() / 60.0

        # Simple, plain-English advice based on curfew safety
        if curfew_margin < 0:
            status = "BREACH"
            minutes_late = abs(round(curfew_margin, 1))
            rec = (
                f"🚨 DON'T GO: You will return {minutes_late} minutes after the 12:30 AM curfew! "
                f"The gate will be locked. Skip tonight or have quick tea to avoid the late register."
            )
        elif curfew_margin <= curfew_buffer_mins:
            status = "CAUTION"
            margin_left = round(curfew_margin, 1)
            rec = (
                f"⚠️ HURRY: You only have {margin_left} minutes to spare before 12:30 AM! "
                f"Walk quickly and choose Plain Maggi or Tea instead of slow egg items."
            )
        else:
            status = "SAFE"
            margin_left = round(curfew_margin, 1)
            rec = (
                f"✅ SAFE TO GO: You have {margin_left} minutes to spare before the 12:30 AM curfew. "
                f"You will reach {hostel} comfortably in time."
            )

        # Compare with Bipul Da's "5 minutes" claim
        claimed_wait = 5.0 if safe_orders_ahead <= 4 else 10.0
        gap = round(estimated_cook_wait - claimed_wait, 1)

        return QueuePrediction(
            item_name=dish_name,
            dish_category=dish_category,
            hostel=hostel,
            orders_ahead=safe_orders_ahead,
            burners_active=safe_burners,
            vendor_promised_mins=claimed_wait,
            estimated_cook_wait_mins=round(estimated_cook_wait, 1),
            walk_one_way_mins=walk_time,
            total_trip_mins=round(total_trip_mins, 1),
            estimated_ready_time=ready_dt.strftime("%I:%M %p"),
            estimated_return_time=return_dt.strftime("%I:%M %p"),
            curfew_time=curfew_dt.strftime("%I:%M %p"),
            curfew_status=status,
            curfew_margin_mins=round(curfew_margin, 1),
            recommendation=rec,
            empirical_error_spread_mins=gap,
        )


if __name__ == "__main__":
    model = NightQueueModel("data.csv")
    print("Summary Stats:", model.get_summary_stats())
