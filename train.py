from ultralytics import YOLO
import torch

def pick_device():
    if torch.cuda.is_available(): return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available(): return "mps"
    return "cpu"

device = pick_device()
print(f"device: {device}")
model = YOLO("models/yolo11n.pt")  # 교통 표지로 선행 학습된 가중치

# 중요한 포인트
# - fliplr=0: 좌/우 반전 금지(좌↔우 의미 뒤집힘 예방)
# - degrees는 0 또는 아주 소폭(±3~5도)
# - 음성 데이터(다른 표지/표지 아님)를 충분히 포함해 FP 억제
results = model.train(
    data="traffic4.yaml",   # 4개 클래스만 정의
    device=device,
    epochs=80,
    imgsz=640,
    batch=16,
    fliplr=0.0,
    degrees=0.0,
    translate=0.05, scale=0.5, shear=0.0,
    hsv_h=0.015, hsv_s=0.7, hsv_v=0.4,
    # 데이터가 적으면 backbone 일부 동결로 안정화
    # freeze=10,
)

# 검증 및 혼동행렬 확인
metrics = model.val(data="traffic4.yaml", device=device, imgsz=640, plots=True)
print(metrics.results_dict)

# 추론
# preds = model("images/test.jpg", device=device, conf=0.25)