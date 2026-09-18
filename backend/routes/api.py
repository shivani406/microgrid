from flask import Blueprint, jsonify, request
from db.queries import fetch_latest_telemetry, fetch_historical_telemetry

api_bp = Blueprint("api", __name__)

@api_bp.route("/status", methods=["GET"])
def get_status():
    latest = fetch_latest_telemetry()
    return jsonify(latest if latest else {"message": "No telemetry recorded yet."}), 200

@api_bp.route("/history", methods=["GET"])
def get_history():
    limit = request.args.get("limit", default=50, type=int)
    records = fetch_historical_telemetry(limit=limit)
    return jsonify(records), 200