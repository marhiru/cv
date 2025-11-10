import cv2

from ultralytics import solutions

cap = cv2.VideoCapture("demo/highway1.mov")
assert cap.isOpened(), "Error reading video file"

w, h, fps = (
    int(cap.get(x))
    for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS)
)
distancecalculator = solutions.DistanceCalculation(
    model="models/yolo12n.pt",
    show=True,
)

while cap.isOpened():
    success, im0 = cap.read()

    if not success:
        print("Video frame is empty or processing is complete.")
        break

    results = distancecalculator(im0)

    print(results)


cap.release()

cv2.destroyAllWindows()
