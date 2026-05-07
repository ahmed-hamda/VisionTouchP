import os
import time
from typing import List, Dict, Any, Tuple

import cv2
import numpy as np
import torch
from ultralytics import YOLO

ALLOWED_EXT = {"jpg", "jpeg", "png", "webp"}


def allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    return filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


def decode_image(file_bytes: bytes) -> np.ndarray:
    arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image data (cannot decode).")
    return img


class YoloDetector:
    def __init__(self, model_path: str = "yolov8n.pt", conf: float = 0.25, imgsz: int = 640) -> None:
        self.model_path = model_path
        self.conf = conf
        self.imgsz = imgsz

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        # Temporarily patch torch.load to allow loading YOLO model
        original_load = torch.load
        def patched_load(*args, **kwargs):
            kwargs.setdefault('weights_only', False)
            return original_load(*args, **kwargs)
        torch.load = patched_load

        try:
            self.model = YOLO(self.model_path)
        finally:
            torch.load = original_load

        self.names = getattr(self.model, "names", {})

    def model_info(self) -> Dict[str, Any]:
        total_classes = len(self.names) if isinstance(self.names, dict) else None
        return {
            "model_name": os.path.basename(self.model_path),
            "model_path": self.model_path,
            "total_classes": total_classes,
            "conf_threshold": self.conf,
            "imgsz": self.imgsz,
        }

    def predict(self, image_bgr: np.ndarray) -> Tuple[List[Dict[str, Any]], int]:
        start = time.perf_counter()

        results = self.model.predict(
            source=image_bgr,
            conf=self.conf,
            imgsz=self.imgsz,
            verbose=False
        )

        objects: List[Dict[str, Any]] = []
        if results:
            r = results[0]
            if r.boxes is not None and len(r.boxes) > 0:
                xyxy = r.boxes.xyxy.cpu().numpy()
                confs = r.boxes.conf.cpu().numpy()
                clss = r.boxes.cls.cpu().numpy().astype(int)

                for (x1, y1, x2, y2), c, k in zip(xyxy, confs, clss):
                    w = max(0.0, float(x2 - x1))
                    h = max(0.0, float(y2 - y1))
                    label = self.names.get(k, str(k)) if isinstance(self.names, dict) else str(k)

                    objects.append({
                        "label": label,
                        "confidence": round(float(c), 4),
                        "bbox": {
                            "x": int(round(float(x1))),
                            "y": int(round(float(y1))),
                            "width": int(round(w)),
                            "height": int(round(h)),
                        }
                    })

        inference_ms = int(round((time.perf_counter() - start) * 1000))
        return objects, inference_ms