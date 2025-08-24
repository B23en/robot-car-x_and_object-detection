from ultralytics import YOLO
import torch

# 디바이스 선택
device = "cuda" if torch.cuda.is_available() else (
    "mps" if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available() else "cpu"
)

# 모델 불러오기
model = YOLO("models/best_15e.pt")

# 이미지 추론
results = model("test/img.jpg", device=device, conf=0.25)
print(results[0].boxes)

# 결과 시각화 및 저장
results[0].plot(show=True, save=True, filename="result.jpg")