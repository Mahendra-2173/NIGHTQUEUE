"""
NightQueue: Flask Web Application & Technical CLI Runner
Grounds wait-time and curfew predictions in empirical data from Gate 1, NIT Silchar.
"""

import sys
import argparse
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from core_engine import NightQueueModel

app = Flask(__name__)
CORS(app)

model = NightQueueModel("data.csv")


# Multi-Page Navigation Routes
@app.route("/")
def index():
    """Main dashboard entrypoint (defaults to Curfew Checker)."""
    return render_template("index.html", initial_page="checker")


@app.route("/checker")
def checker_page():
    """Curfew Checker page."""
    return render_template("index.html", initial_page="checker")


@app.route("/data")
def data_page():
    """Stall Data page (20 verified observations & item statistics)."""
    return render_template("index.html", initial_page="data")


@app.route("/story")
def story_page():
    """The Fieldwork Story page (NIT Silchar context)."""
    return render_template("index.html", initial_page="story")


@app.route("/test")
def test_page():
    """Simple Test and Reliability Diagnostics page."""
    return render_template("index.html", initial_page="test")


@app.route("/photos/<path:filename>")
def serve_photo(filename):
    """Serves fieldwork timestamped photos."""
    return send_from_directory("photos", filename)


# REST API Endpoints
@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Returns empirical summary statistics calculated from data.csv."""
    stats = model.get_summary_stats()
    return jsonify(stats)


@app.route("/api/data", methods=["GET"])
def get_data_rows():
    """Returns all validated observational records from data.csv."""
    if model.valid_df is not None and not model.valid_df.empty:
        records = model.valid_df.fillna("").to_dict(orient="records")
        return jsonify(records)
    return jsonify([])


@app.route("/api/item-stats", methods=["GET"])
def get_item_statistics():
    """Returns food-item-wise mean, median, min, max, and std statistics."""
    item_stats = model.get_item_statistics()
    return jsonify(item_stats)


@app.route("/api/audit", methods=["GET"])
def get_dataset_audit():
    """Returns the comprehensive dataset validation and health report."""
    rep = model.load_and_validate_dataset()
    return jsonify(rep.__dict__)


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Main prediction endpoint. Uses item-level empirical statistics,
    queue congestion modeling, walking transit matrix, and date-aware curfew feasibility.
    """
    payload = request.get_json() or {}

    dish_name = payload.get("dish_name", "Double Egg Maggi")
    dish_category = payload.get("dish_category", "maggi")
    hostel = payload.get("hostel", "Hostel 7")
    orders_ahead = payload.get("orders_ahead", 4)
    burners_active = payload.get("burners_active", 2)
    current_time = payload.get("current_time", "23:45")
    curfew_time = payload.get("curfew_time", "00:30")
    curfew_buffer = payload.get("curfew_buffer", 5.0)

    prediction = model.predict_wait_and_curfew(
        dish_name=dish_name,
        dish_category=dish_category,
        hostel=hostel,
        orders_ahead=orders_ahead,
        burners_active=burners_active,
        current_time_str=current_time,
        curfew_time_str=curfew_time,
        curfew_buffer_mins=float(curfew_buffer),
    )

    return jsonify(prediction.__dict__)


@app.route("/api/test-bad-row", methods=["POST"])
def test_bad_row():
    """
    Defensively sanitizes bad or adversarial inputs (negative orders, 0 burners)
    and demonstrates safe software degradation without crashing.
    """
    payload = request.get_json() or {}
    raw_orders = payload.get("orders_ahead", -5)
    raw_burners = payload.get("burners_active", 0)
    dish_category = payload.get("dish_category", "unknown_category")
    current_time = payload.get("current_time", "99:99")

    # Defensive sanitization
    sanitized_orders = max(0, int(raw_orders)) if isinstance(raw_orders, (int, float)) else 0
    sanitized_burners = max(1, min(4, int(raw_burners))) if isinstance(raw_burners, (int, float)) else 2

    try:
        prediction = model.predict_wait_and_curfew(
            dish_name="Stress Test Item",
            dish_category=dish_category,
            hostel="Hostel 7",
            orders_ahead=sanitized_orders,
            burners_active=sanitized_burners,
            current_time_str=current_time,
        )
        return jsonify({
            "status": "DEFENDED_SUCCESSFULLY",
            "sanitized_orders_ahead": sanitized_orders,
            "sanitized_burners_active": sanitized_burners,
            "estimated_cook_wait_mins": prediction.historical_prep_mins + prediction.queue_wait_mins,
            "defense_note": (
                f"Fixed bad inputs safely: orders({raw_orders}) -> {sanitized_orders}, "
                f"burners({raw_burners}) -> {sanitized_burners}. Time fallback applied safely."
            )
        })
    except Exception as e:
        return jsonify({
            "status": "ERROR_HANDLED",
            "error_detail": str(e)
        }), 400


def run_cli():
    """Runs a complete technical evaluation report in terminal mode."""
    print("=" * 70)
    print("🌙 NightQueue: NIT Silchar Gate 1 Queuing Model (Technical CLI Report)")
    print("=" * 70)

    rep = model.validation_report
    print("\n[1] DATASET INTEGRITY & VALIDATION AUDIT (data.csv):")
    print(f"  • Validation Status:       {'PASS (Clean)' if rep.is_valid else 'FAIL'}")
    print(f"  • Total Rows Read:         {rep.total_rows_read}")
    print(f"  • Valid Historical Rows:   {rep.valid_rows_count}")
    print(f"  • Excluded Records:        {rep.excluded_rows_count}")
    print(f"  • Missing Values:          {rep.missing_values_count}")
    print(f"  • Duplicate IDs:           {rep.duplicate_ids_count}")

    print("\n[2] FOOD-ITEM HISTORICAL PREPARATION TIME STATISTICS:")
    for item, s in model.get_item_statistics().items():
        print(f"  • {item:18}: n={s['count']} | mean={s['mean_actual_mins']}m | median={s['median_actual_mins']}m | min={s['min_actual_mins']}m | max={s['max_actual_mins']}m | std={s['std_actual_mins']}m")

    stats = model.get_summary_stats()
    print("\n[3] EMPIRICAL QUEUING EVIDENCE:")
    print(f"  • Bipul Da's Claimed Mean: {stats['avg_claimed_mins']} mins ('Bas 5 minute')")
    print(f"  • Actual Measured Mean:    {stats['avg_actual_mins']} mins")
    print(f"  • Underestimation Gap:     +{stats['avg_underestimation_gap']} mins late")
    print(f"  • Curfew Stress / Sprints: {stats['curfew_incident_rate_pct']}% ({stats['curfew_incident_count']} of {stats['total_orders']} observed visits)")
    print(f"  • Confirmed Late Entries:  {stats['confirmed_late_entry_pct']}% ({stats['confirmed_late_entry_count']} of {stats['total_orders']} documented register entries)")
    print(f"  • Marginal Delay/Order:    ~{stats['queue_penalty_per_order']} mins/order")

    print("\n[4] SAMPLE PREDICTION: 23:45 IST, Hostel 7 Student, Bun Omelette, 6 orders ahead:")
    pred = model.predict_wait_and_curfew(
        dish_name="Bun Omelette",
        dish_category="egg_toast",
        hostel="Hostel 7",
        orders_ahead=6,
        burners_active=2,
        current_time_str="23:45",
        curfew_time_str="00:30",
    )
    print("  • 5-Milestone Journey Timeline:")
    print(f"    1. Depart Hostel -> Reach Stall:  {pred.stall_arrival_time} ({pred.walk_to_stall_mins} mins walk)")
    print(f"    2. Kitchen Delay (Prep + Queue):  {pred.food_prep_and_wait_mins} mins (Base: {pred.historical_prep_mins}m, Queue: {pred.queue_wait_mins}m)")
    print(f"    3. Food Ready Handover:          {pred.food_ready_time}")
    print(f"    4. Return Walk -> Room Return:   {pred.room_return_time} ({pred.walk_return_mins} mins return walk)")
    print(f"    5. Curfew Margin:                {pred.remaining_curfew_mins:+.1f} mins vs {pred.curfew_time} deadline")
    print(f"  • Uncertainty Buffer:              ±{pred.uncertainty_buffer_mins} mins ({pred.expected_range})")
    print(f"  • Latest Departure Time:           {pred.departure_deadline}")
    print(f"  • Curfew Feasibility Verdict:      [{pred.curfew_status}]")
    print(f"  • Practical Advice:                {pred.recommendation}")
    print(f"  • Disclaimer:                      {pred.prediction_disclaimer}")

    print("\n[5] BAD-ROW STRESS TEST (Handling negative queue & 0 burners):")
    bad_pred = model.predict_wait_and_curfew(
        dish_name="Corrupt Input",
        dish_category="invalid",
        hostel="Unknown Hostel",
        orders_ahead=-20,
        burners_active=0,
        current_time_str="99:99",
    )
    print(f"  • Handled cleanly without crash. Fallback wait: {bad_pred.historical_prep_mins + bad_pred.queue_wait_mins} mins")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NightQueue NIT Silchar")
    parser.add_argument("--cli", action="store_true", help="Run in technical CLI mode")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind web server (default: 5000)")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        print(f"🚀 Starting NightQueue Web Server at http://127.0.0.1:{args.port}...")
        app.run(host="127.0.0.1", port=args.port, debug=False)
