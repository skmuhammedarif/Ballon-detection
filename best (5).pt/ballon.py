import cv2
from ultralytics import YOLO
import time

# Load model
model = YOLO(r"C:\Users\natur\OneDrive\Documents\Best\best (5).pt")

cap = cv2.VideoCapture(0)

# Reduce camera resolution (BIG impact)
cap.set(3, 640)   # width
cap.set(4, 480)   # height

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # 🔥 Skip frames (huge performance boost)
    if frame_count % 2 != 0:
        continue

    start = time.time()

    # 🔥 Fast inference settings
    results = model.predict(
        frame,
        imgsz=640,       # balance speed + accuracy
        conf=0.5,
        verbose=False
    )

    annotated = results[0].plot()

    # FPS display
    fps = 1 / (time.time() - start)
    cv2.putText(annotated, f"FPS: {int(fps)}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Balloon Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()