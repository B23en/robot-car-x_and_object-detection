from ultralytics import YOLO
import torch
from pathlib import Path

def pick_device():
    if torch.cuda.is_available(): return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available(): return "mps"
    return "cpu"

device = pick_device()
print(f"device: {device}")
model = YOLO("models/yolo11s.pt")

ROOT = Path("/Users/sonwonbin/vscode/Project/Robot-car-project/merged_dataset")

yaml_dir = ROOT / "traffic4.yaml"

results = model.train(
    data=yaml_dir,
    device=device,
    epochs=40,
    imgsz=640,
    batch=16,
    fliplr=0.0,
    degrees=0.0,
    translate=0.05, scale=0.5, shear=2.0,
    hsv_h=0.015, hsv_s=0.7, hsv_v=0.4,
    # mosaic=0.7, close_mosaic=5,
    freeze=0,
    patience=10
)

metrics = model.val(data=yaml_dir, device=device, imgsz=640, plots=True)
print(metrics.results_dict)

# preds = model("images/test.jpg", device=device, conf=0.25)