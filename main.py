import cv2
from uniface import SCRFD
from uniface.constants import SCRFDWeights

from features.timer import Timer

detector = SCRFD(
    model_name=SCRFDWeights.SCRFD_10G_KPS,
    conf_thresh=0.5,
    nms_thresh=0.4,
    input_size=(640, 640),
)
image = cv2.imread("./tomhanks01.jpeg", cv2.IMREAD_COLOR)
timer = Timer(True)

if image is not None:
    faces = detector.detect(image)

    for face in faces:
        bbox = face["bbox"]
        confidence = face["confidence"]
        landmarks = face["landmarks"]

        result = f"bouding boxes: {bbox}\nconfidence: {confidence:.2}\nlandmarks: {landmarks}"
        print(f"{result}")

        cv2.imshow("Tomhanks", image)
        timer_debug = timer.debug()
        cv2.waitKey(0)
        exit()


def main() -> int:
    return 0


if __name__ == "__main__":
    main()
