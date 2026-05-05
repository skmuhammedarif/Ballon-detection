import cv2
from ultralytics import YOLO
import time

# 🔥 Load ONNX model with task
model = YOLO("best (2).onnx", task="detect")

cap = cv2.VideoCapture(0)

# Camera resolution (low = faster)
cap.set(3, 640)
cap.set(4, 480)

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # 🔥 Skip frames (performance boost)
    if frame_count % 2 != 0:
        continue

    start = time.time()

    # 🔥 Resize to match ONNX input (IMPORTANT FIX)
    resized = cv2.resize(frame, (1024, 1024))

    results = model.predict(
        resized,
        imgsz=1024,   # must match model
        conf=0.5,
        verbose=False
    )

    annotated = results[0].plot()

    # 🔥 Resize back for display
    annotated = cv2.resize(annotated, (640, 480))

    # FPS display
    fps = 1 / (time.time() - start)
    cv2.putText(annotated, f"FPS: {int(fps)}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Balloon Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()