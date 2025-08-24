from ultralytics import YOLO
import torch
from pathlib import Path

def pick_device():
    if torch.cuda.is_available(): return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available(): return "mps"
    return "cpu"

device = pick_device()
print(f"device: {device}")
model = YOLO("models/best.pt")

ROOT = Path("/Users/sonwonbin/vscode/Project/Robot-car-project/dataset_street_signs")

yaml_dir = ROOT / "street_signs.yaml"

results = model.train(
    data=yaml_dir,
    device=device,
    epochs=50,
    imgsz=640,
    batch=16,
    fliplr=0.0,
    degrees=0.0,
    translate=0.05, scale=0.5, shear=0.0,
    hsv_h=0.015, hsv_s=0.7, hsv_v=0.4,
    freeze=10,
    patience=5
)

metrics = model.val(data=yaml_dir, device=device, imgsz=640, plots=True)
print(metrics.results_dict)

# preds = model("images/test.jpg", device=device, conf=0.25)