from ultralytics import YOLO
import torch

# 디바이스 선택
device = "cuda" if torch.cuda.is_available() else (
    "mps" if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available() else "cpu"
)

# 모델 불러오기
model = YOLO("models/best_s_adv.pt")

# 이미지 추론
results = model("test/img.jpg", device=device, conf=0.7)
print(results[0].boxes)

# 결과 시각화 및 저장
results[0].plot(show=True, save=False, filename="result.jpg")

for box in results[0].boxes:
    xyxy = box.xyxy[0].tolist()
    conf = float(box.conf[0])
    cls_id = int(box.cls[0])
    cls_name = results[0].names[cls_id]