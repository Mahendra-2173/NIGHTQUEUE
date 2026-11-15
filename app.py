"""
NightQueue: Simple Web App & CLI for NIT Silchar Students
Calculates cooking wait times and hostel curfew safety for Bipul Da's stall at Gate 1.
"""

import sys
import argparse
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from core_engine import NightQueueModel

app = Flask(__name__)
CORS(app)

model = NightQueueModel("data.csv")


# Multi-page web routes
@app.route("/")
def index():
    """Main home page (Curfew Checker)."""
    return render_template("index.html", initial_page="checker")


@app.route("/checker")
def checker_page():
    """Curfew Checker page."""
    return render_template("index.html", initial_page="checker")


@app.route("/data")
def data_page():
    """Stall Data page (20 Real Orders)."""
    return render_template("index.html", initial_page="data")


@app.route("/story")
def story_page():
    """The Story page (About Bipul Da and NIT Silchar)."""
    return render_template("index.html", initial_page="story")


@app.route("/test")
def test_page():
    """Simple Test and How It Works page."""
    return render_template("index.html", initial_page="test")


# Simple API endpoints
@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Returns summary numbers from the 20 real stall visits."""
    stats = model.get_summary_stats()
    return jsonify(stats)


@app.route("/api/data", methods=["GET"])
def get_data_rows():
    """Returns all 20 real orders recorded at the stall."""
    if model.df is not None and not model.df.empty:
        records = model.df.fillna("").to_dict(orient="records")
        return jsonify(records)
    return jsonify([])


@app.route("/api/predict", methods=["POST"])
def predict():
    """Calculates wait time and tells if the student can make curfew."""
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
    Safely handles bad or unusual inputs (like negative orders or 0 burners)
    so the app never crashes.
    """
    payload = request.get_json() or {}
    raw_orders = payload.get("orders_ahead", -5)
    raw_burners = payload.get("burners_active", 0)
    dish_category = payload.get("dish_category", "unknown_category")
    current_time = payload.get("current_time", "99:99")

    # Clean up inputs safely
    sanitized_orders = max(0, int(raw_orders)) if isinstance(raw_orders, (int, float)) else 0
    sanitized_burners = max(1, int(raw_burners)) if isinstance(raw_burners, (int, float)) else 1

    try:
        prediction = model.predict_wait_and_curfew(
            dish_name="Test Food",
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
                f"burners({raw_burners}) -> {sanitized_burners}. Safe wait time estimated."
            )
        })
    except Exception as e:
        return jsonify({
            "status": "ERROR_HANDLED",
            "error_detail": str(e)
        }), 400


def run_cli():
    """Runs a quick simple terminal report."""
    print("=" * 60)
    print("🌙 NightQueue: NIT Silchar Food Wait & Curfew Checker")
    print("=" * 60)

    stats = model.get_summary_stats()
    print("\n[1] Stall Visit Summary (from data.csv):")
    print(f"  • Real Orders Tracked:      {stats['total_orders']}")
    print(f"  • What Bipul Da Promised:   {stats['avg_claimed_mins']} mins")
    print(f"  • Actual Wait Time:         {stats['avg_actual_mins']} mins")
    print(f"  • The Difference:           +{stats['avg_underestimation_gap']} mins late")
    print(f"  • Students Late for Curfew: {stats['curfew_breach_rate_pct']}% of observed visits")

    print("\n[2] Sample Student Check (Hostel 7, 11:45 PM, 6 people ahead):")
    pred = model.predict_wait_and_curfew(
        dish_name="Bun Omelette",
        dish_category="egg_toast",
        hostel="Hostel 7",
        orders_ahead=6,
        burners_active=2,
        current_time_str="23:45",
        curfew_time_str="00:30",
    )
    print(f"  • Estimated Cook Time:      {pred.estimated_cook_wait_mins} mins (Bipul Da claims: {pred.vendor_promised_mins} mins)")
    print(f"  • Total Trip Time:          {pred.total_trip_mins} mins ({pred.walk_one_way_mins} mins walk each way)")
    print(f"  • Time You Reach Room:      {pred.estimated_return_time}")
    print(f"  • Hostel Curfew:            {pred.curfew_time}")
    print(f"  • Status:                   [{pred.curfew_status}]")
    print(f"  • Advice:                   {pred.recommendation}")

    print("\n[3] Simple Input Safety Test (Testing negative numbers & 0 burners):")
    bad_pred = model.predict_wait_and_curfew(
        dish_name="Test Food",
        dish_category="invalid",
        hostel="Hostel 7",
        orders_ahead=-10,
        burners_active=0,
        current_time_str="99:99",
    )
    print(f"  • Handled safely without error! Estimated wait: {bad_pred.estimated_cook_wait_mins} mins")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NightQueue NIT Silchar")
    parser.add_argument("--cli", action="store_true", help="Run in terminal CLI mode")
    parser.add_argument("--port", type=int, default=5000, help="Port to run web app (default: 5000)")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        print(f"🚀 Starting NightQueue Web App at http://127.0.0.1:{args.port}...")
        app.run(host="127.0.0.1", port=args.port, debug=False)
