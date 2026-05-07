import os
from flask import Flask
from flask_cors import CORS

from routes.detection import detection_bp
from services.detector import YoloDetector


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL_PATH = os.path.join(BASE_DIR, "model", "best.pt")


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    # Config
    model_path = os.getenv("YOLO_MODEL_PATH", DEFAULT_MODEL_PATH)
    conf = float(os.getenv("CONF_THRESHOLD", "0.25"))
    imgsz = int(os.getenv("IMG_SIZE", "640"))

    # Load model once
    try:
        detector = YoloDetector(model_path=model_path, conf=conf, imgsz=imgsz)
        app.config["DETECTOR"] = detector
        print(f"[OK] YOLO loaded: {model_path}")
    except Exception as e:
        app.config["DETECTOR"] = None
        print(f"[ERROR] Failed to load YOLO model: {e}")

    # Register routes
    app.register_blueprint(detection_bp, url_prefix="/api")
    return app


app = create_app()

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host=host, port=port, debug=debug)