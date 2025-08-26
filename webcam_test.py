import cv2
from ultralytics import YOLO

from check_bbox import CheckBbox
from pprint import pprint

model = YOLO("models/best_s_adv.pt")
model.to("mps")
cap = cv2.VideoCapture(0)
checker = CheckBbox()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    results = model(frame, conf=0.7)

    # Update stable detection state
    curr = checker.check(results)  # returns dict or {}
    print(curr)

    for r in results:
        annotated_frame = r.plot()

        # Overlay current confirmed class (if any)
        label = curr if curr != "none" else None
        if label:
            cv2.putText(
                annotated_frame,
                f"CONFIRMED: {label}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.0,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

        cv2.imshow("YOLO Webcam", annotated_frame)

    # ESC(27) 누르면 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()