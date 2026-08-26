from flask import Flask, jsonify, request, render_template
import os
import socket

from db import (
    device_exists,
    get_devices,
    get_measurements,
    get_latest_measurement,
    get_measurements_for_device,
    insert_measurement,
)
from validation import validate_measurement
from cache import get_latest_from_cache, set_latest_in_cache

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "v1")
POD_NAME = socket.gethostname()


@app.get("/")
def dashboard():
    return render_template("index.html", version=APP_VERSION, pod=POD_NAME)


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "version": APP_VERSION,
        "pod": POD_NAME,
    }), 200


@app.get("/devices")
def devices():
    return jsonify(get_devices()), 200


@app.get("/measurements")
def measurements():
    return jsonify(get_measurements()), 200


@app.get("/devices/<device_id>/latest")
def latest(device_id):
   
    cached_measurement = get_latest_from_cache(device_id)

    if cached_measurement is not None:
        return jsonify(cached_measurement), 200

    if not device_exists(device_id):
        return jsonify({"error": f"Device {device_id} not found"}), 404

    measurement = get_latest_measurement(device_id)

    if measurement is None:
        return jsonify({"error": f"No measurements found for device {device_id}"}), 404

    set_latest_in_cache(device_id, measurement)

    return jsonify(measurement), 200


@app.get("/devices/<device_id>/measurements")
def device_history(device_id):
    
    if not device_exists(device_id):
        return jsonify({"error": f"Device {device_id} not found"}), 404

    history = get_measurements_for_device(device_id)

    return jsonify(history), 200
    
    
@app.post("/measurements")
def create_measurement():
    data = request.get_json(silent=True) or {}
    errors = validate_measurement(data)

    if errors:
        print(f"INVALID measurement from {data.get('deviceId', 'unknown')}: {errors}")
        return jsonify({"errors": errors}), 400

    device_id = data.get("deviceId")

    if not device_exists(device_id):
        return jsonify({"error": f"Device {device_id} not found"}), 400

    saved_measurement = insert_measurement(data)

    set_latest_in_cache(device_id, saved_measurement)

    print(f"VALID measurement received: {data}")
    return jsonify({"status": "created", "measurement": saved_measurement}), 201


@app.get("/statistics")
def statistics():
    # ⭐ Utmaning:
    # Returnera antal devices, antal measurements, avg temp etc.
    return jsonify({"message": "Optional challenge"}), 501


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
