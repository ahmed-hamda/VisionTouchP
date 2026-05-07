import os
from flask import Blueprint, request, jsonify, current_app

from services.detector import allowed_file, decode_image

detection_bp = Blueprint("detection", __name__)


@detection_bp.get("/health")
def health():
    detector = current_app.config.get("DETECTOR", None)
    return jsonify({
        "status": "running",
        "model_loaded": detector is not None
    })


@detection_bp.get("/model-info")
def model_info():
    detector = current_app.config.get("DETECTOR", None)
    if detector is None:
        return jsonify({"status": "error", "message": "Model not loaded"}), 500

    return jsonify({
        "status": "success",
        **detector.model_info()
    })


@detection_bp.post("/detect")
def detect():
    detector = current_app.config.get("DETECTOR", None)
    if detector is None:
        return jsonify({"status": "error", "message": "Model not loaded"}), 500

    if "image" not in request.files:
        return jsonify({"status": "error", "message": "Missing 'image' field"}), 400

    f = request.files["image"]
    if f.filename == "":
        return jsonify({"status": "error", "message": "Empty filename"}), 400

    if not allowed_file(f.filename):
        return jsonify({
            "status": "error",
            "message": "Unsupported file type. Allowed: jpg, jpeg, png, webp"
        }), 400

    try:
        img_bytes = f.read()
        image = decode_image(img_bytes)

        objects, inference_ms = detector.predict(image)

        return jsonify({
            "status": "success",
            "objects": objects,
            "count": len(objects),
            "inference_time_ms": inference_ms
        })
    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as e:
        # In prod: don't expose details
        return jsonify({"status": "error", "message": "Server error", "details": str(e)}), 500