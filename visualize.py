import cv2
from ultralytics import YOLO
import torch

# 1. 모델 로드
# model = YOLO(r"models/traffic_sign_detection_model.pt")  # 모델 경로
model = YOLO("models/yolo11s.pt")

# 디바이스 자동 감지 및 지정
if torch.cuda.is_available():
    device = torch.device("cuda")
elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
model.to(device)
print(f"✅ Using device: {device}")

# 2. 이미지 불러오기
image_path = r"images/0000819.jpg"   # 탐지할 이미지 경로
img = cv2.imread(image_path)

# 3. 탐지 수행
results = model(img, verbose=False)

# 4. 결과 처리 및 출력
for r in results:
    boxes = r.boxes
    for box in boxes:
        # 좌표, 클래스, confidence 추출
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        
        print(f"Class: {cls}, Confidence: {conf:.2f}, BBox: {(x1, y1, x2, y2)}")
        
        # 시각화 (Bounding Box + 라벨)
        label = f"{cls} {conf:.2f}"
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(img, label, (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# 5. 결과 표시
cv2.imshow("Detection Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 6. 결과 저장 (선택 사항)
# cv2.imwrite("output.jpg", img)
# print("✅ 탐지 결과 저장: output.jpg")