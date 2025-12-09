import cv2
from uniface import SCRFD
from uniface.constants import SCRFDWeights
import time
from features.timer import Timer


class DetectorEngine:
    def __init__(self, model, filename: str = "./tomhanks01.jpeg") -> None:
        self.model: SCRFD = model
        self.filename = filename
        # dependencies = cv2.imread(self.filename, cv2.IMREAD_COLOR)
        dependencies = None

        assert dependencies is not None, (
            f"\n[\x1b[48;5;1m\x1b[38;5;0m  VariableError  \x1b[0m] '{dependencies}' cannot be value of variable: 'dependencies'"
        )

        if dependencies is not None:
            faces = model.detect(dependencies)

            for face in faces:
                cv2.imshow("Tomhanks", dependencies)
                cv2.waitKey(0)


class DetectorExecution:
    def __init__(self, model) -> None:
        super().__init__()
        self.elapsed = time.time()
        self.model = model
        model = DetectorExecution.model_selection(self)

        DetectorEngine(model)
        DetectorExecution._elapsing(self)

    def model_selection(self):
        if self.model is None:
            return SCRFD(
                model_name=SCRFDWeights.SCRFD_10G_KPS,
                conf_thresh=0.5,
                nms_thresh=0.4,
                input_size=(640, 640),
            )
        else:
            return self.model

    def _elapsing(self):
        timer = Timer(self.elapsed)
        return timer.exec_time()


class Detector:
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.model = kwargs.get("model", None)

        DetectorExecution(self.model)
