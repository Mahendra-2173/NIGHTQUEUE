"""
NightQueue: Flask Web Application & CLI for NIT Silchar Students & Stall Operator
Predicts food wait times, curfew feasibility, and empowers Bipul Da with honest queue quotes.
"""

import sys
import argparse
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from core_engine import NightQueueModel

app = Flask(__name__)
CORS(app)

model = NightQueueModel("data.csv")


# Web Page Routes
@app.route("/")
def index():
    """Main home dashboard (defaults to Curfew Checker)."""
    return render_template("index.html", initial_page="checker")


@app.route("/checker")
def checker_page():
    """Student Curfew & Queue Radar page."""
    return render_template("index.html", initial_page="checker")


@app.route("/owner")
def owner_page():
    """Stall Owner (Bipul Da) Order Manager page."""
    return render_template("index.html", initial_page="owner")


@app.route("/data")
def data_page():
    """Stall Data page (20 Real Observations)."""
    return render_template("index.html", initial_page="data")


@app.route("/story")
def story_page():
    """The Fieldwork Story page (NIT Silchar Gate 1)."""
    return render_template("index.html", initial_page="story")


@app.route("/test")
def test_page():
    """Simple Test & Diagnostics page."""
    return render_template("index.html", initial_page="test")


# REST API Endpoints
@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Returns empirical summary statistics calculated from data.csv."""
    stats = model.get_summary_stats()
    return jsonify(stats)


@app.route("/api/data", methods=["GET"])
def get_data_rows():
    """Returns all 20 real observational records from data.csv."""
    if model.df is not None and not model.df.empty:
        records = model.df.fillna("").to_dict(orient="records")
        return jsonify(records)
    return jsonify([])


@app.route("/api/audit", methods=["GET"])
def get_dataset_audit():
    """Returns dataset health and integrity audit (Section 3 compliance)."""
    audit = model.validate_dataset()
    return jsonify(audit.__dict__)


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Main prediction endpoint. Calculates cook delay from empirical observations,
    walk time, departure deadline, curfew feasibility, and confidence interval.
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
    and demonstrates safe software degradation.
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
            "estimated_cook_wait_mins": prediction.estimated_cook_wait_mins,
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
    print("=" * 68)
    print("🌙 NightQueue: NIT Silchar Gate 1 Queuing Model (Technical CLI Report)")
    print("=" * 68)

    audit = model.validate_dataset()
    print("\n[1] DATASET INTEGRITY & VALIDATION AUDIT (data.csv):")
    print(f"  • Validation Status:       {'PASS (Clean)' if audit.is_valid else 'FAIL'}")
    print(f"  • Total Genuine Rows:      {audit.total_rows}")
    print(f"  • Missing Values:          {audit.missing_values_count}")
    print(f"  • Duplicate IDs:           {audit.duplicate_ids_count}")
    print(f"  • Categories Verified:     {', '.join(audit.categories_present)}")

    stats = model.get_summary_stats()
    print("\n[2] EMPIRICAL FIELDWORK EVIDENCE:")
    print(f"  • Bipul Da's Claimed Mean: {stats['avg_claimed_mins']} mins ('Bas 5 minute')")
    print(f"  • Actual Measured Mean:    {stats['avg_actual_mins']} mins")
    print(f"  • Underestimation Gap:     +{stats['avg_underestimation_gap']} mins late")
    print(f"  • Curfew Breach Rate:      {stats['curfew_breach_rate_pct']}% of observed students")
    print(f"  • Marginal Queue Delay:    ~{stats.get('queue_penalty_per_order', 2.3)} mins per waiting order")

    print("\n[3] SAMPLE EVALUATION: 23:45 IST, Hostel 7 Student, Bun Omelette, 6 orders ahead:")
    pred = model.predict_wait_and_curfew(
        dish_name="Bun Omelette",
        dish_category="egg_toast",
        hostel="Hostel 7",
        orders_ahead=6,
        burners_active=2,
        current_time_str="23:45",
        curfew_time_str="00:30",
    )
    print(f"  • Estimated Cook Wait:     {pred.estimated_cook_wait_mins} mins (Bipul Da claims: {pred.vendor_promised_mins}m)")
    print(f"  • Walk Time (Hostel 7):    {pred.walk_one_way_mins} mins each way ({pred.total_trip_mins}m total trip)")
    print(f"  • Latest Departure Time:   {pred.departure_deadline}")
    print(f"  • Estimated Room Return:   {pred.estimated_return_time}")
    print(f"  • Curfew Deadline:         {pred.curfew_time}")
    print(f"  • Curfew Status:           [{pred.curfew_status}] (Margin: {pred.curfew_margin_mins} mins)")
    print(f"  • Advice:                  {pred.recommendation}")
    print(f"  • Empirical Confidence:    {pred.confidence_interval}")

    print("\n[4] BAD-ROW STRESS TEST (Handling negative queue & 0 burners):")
    bad_pred = model.predict_wait_and_curfew(
        dish_name="Stress Item",
        dish_category="invalid_category",
        hostel="Unknown Hostel",
        orders_ahead=-20,
        burners_active=0,
        current_time_str="99:99",
    )
    print(f"  • Handled cleanly without crash. Fallback wait: {bad_pred.estimated_cook_wait_mins} mins")
    print("=" * 68)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NightQueue NIT Silchar")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode instead of web server")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind web server (default: 5000)")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        print(f"🚀 Starting NightQueue Web Server at http://127.0.0.1:{args.port}...")
        app.run(host="127.0.0.1", port=args.port, debug=False)
