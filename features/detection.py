import time
import cv2
from typing import Optional, List, Dict, Any, Protocol, runtime_checkable

from uniface import SCRFD
from uniface.constants import SCRFDWeights

from features.timer import Timer


@runtime_checkable
class RunnerProtocol(Protocol):
    def run(self) -> List[Dict[str, Any]]: ...


@runtime_checkable
class WorkerProtocol(Protocol):
    def execute(self) -> Any: ...


class ModelFactory:
    @staticmethod
    def create(model: Optional[SCRFD] = None) -> SCRFD:
        if model is not None:
            return model

        return SCRFD(
            model_name=SCRFDWeights.SCRFD_10G_KPS,
            conf_thresh=0.5,
            nms_thresh=0.4,
            input_size=(640, 640),
        )


class FaceDetectorEngine:
    def __init__(self, model: SCRFD):
        self.model = model

    def detect(self, image) -> List[Dict[str, Any]]:
        return self.model.detect(image)


class BuiltinRunner:
    def __init__(
        self,
        image_path: str,
        model: SCRFD,
        show: bool = True,
    ):
        self.image_path = image_path
        self.show = show
        self.engine = FaceDetectorEngine(model)

    def _load_image(self):
        image = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
        if image is None:
            raise FileNotFoundError(f"Image not found: {self.image_path}")
        return image

    def run(self) -> List[Dict[str, Any]]:
        image = self._load_image()

        timer = Timer(time.time())
        faces = self.engine.detect(image)
        elapsed = timer.exec_time()

        self._log_results(faces, elapsed)

        if self.show:
            self._display(image)

        return faces

    def _log_results(self, faces, elapsed: float):
        print(f"\nFaces detected: {len(faces)}")
        print(f"Elapsed time: {elapsed:.4f}s\n")

        for idx, face in enumerate(faces, start=1):
            print(f"[Face {idx}]")
            print(f"  Bounding box : {face.get('bbox')}")
            print(f"  Confidence   : {face.get('confidence')}")
            print(f"  Landmarks    : {face.get('landmarks')}\n")

    def _display(self, image):
        cv2.imshow("Face Detection", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class Detector:
    def __init__(
        self,
        image_path: Optional[str] = None,
        model: Optional[SCRFD] = None,
        runner: Optional[RunnerProtocol] = None,
        worker: Optional[WorkerProtocol] = None,
        show: bool = True,
    ):
        self.model = ModelFactory.create(model)

        if worker is not None:
            self.worker = worker
            self.runner = None
            return

        if runner is not None:
            self.runner = runner
            self.worker = None
            return

        if image_path is None:
            raise ValueError("image_path is required when no runner/worker is provided")

        self.runner = BuiltinRunner(
            image_path=image_path,
            model=self.model,
            show=show,
        )
        self.worker = None

    def run(self):
        if self.worker is not None:
            return self.worker.execute()

        if self.runner is not None:
            return self.runner.run()

        raise RuntimeError("Detector is not properly configured")
