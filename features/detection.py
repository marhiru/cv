import cv2
from uniface import SCRFD
from uniface.constants import SCRFDWeights
import time
from features.timer import Timer


class DetectorEngine:
    def __init__(self, model: SCRFD, filename: str = "./tomhanks01.jpeg") -> None:
        self.model = model
        self.filename = filename

        dependencies = DetectorEngine.dependencies(self)

        if dependencies is not None:
            faces = model.detect(dependencies)

            for face in faces:
                bbox = face["bbox"]
                confidence = face["confidence"]
                landmarks = face["landmarks"]

                result = f"bouding boxes: {bbox}\nconfidence: {confidence:.2}\nlandmarks: {landmarks}"
                print(f"{result}")

                cv2.imshow("Tomhanks", dependencies)
                cv2.waitKey(0)
                pass

    def dependencies(self):
        return cv2.imread(self.filename, cv2.IMREAD_COLOR)


class DetectorExecution:
    def __init__(self, model) -> None:
        self.elapsed = time.time()

        DetectorEngine(model)
        DetectorExecution._elapsing(self)

    def _elapsing(self):
        timer = Timer(self.elapsed)
        return timer.exec_time()


class Detector:
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        model = kwargs.get("model", SCRFD)
        self.model = model

        model = Detector.model(self)
        DetectorExecution(model)

    def model(self):
        if self.model is None:
            return SCRFD(
                model_name=SCRFDWeights.SCRFD_10G_KPS,
                conf_thresh=0.5,
                nms_thresh=0.4,
                input_size=(640, 640),
            )
        else:
            return self.model
