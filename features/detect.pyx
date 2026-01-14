# cython: language_level=3, boundscheck=False, wraparound=False

import time
import cv2

from uniface import SCRFD
from uniface.constants import SCRFDWeights

from features.timer import Timer


# =========================================================
# Model Factory (Python-level)
# =========================================================

cdef object create_model(object model):
    if model is not None:
        return model

    return SCRFD(
        model_name=SCRFDWeights.SCRFD_10G_KPS,
        conf_thresh=0.5,
        nms_thresh=0.4,
        input_size=(640, 640),
    )


# =========================================================
# Face Detector Engine
# =========================================================

cdef class FaceDetectorEngine:
    cdef object model

    def __cinit__(self, object model):
        self.model = model

    cpdef list detect(self, object image):
        return self.model.detect(image)


# =========================================================
# Builtin Runner
# =========================================================

cdef class BuiltinRunner:
    cdef:
        object image_path
        bint show
        FaceDetectorEngine engine

    def __cinit__(self, object image_path, object model, bint show=True):
        self.image_path = image_path
        self.show = show
        self.engine = FaceDetectorEngine(model)

    cdef object _load_image(self):
        cdef object image = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
        if image is None:
            raise FileNotFoundError(f"Image not found: {self.image_path}")
        return image

    cdef void _display(self, object image):
        cv2.imshow("Face Detection", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    cdef void _log_results(self, list faces, double elapsed):
        cdef int i
        print(f"\nFaces detected: {len(faces)}")
        print(f"Elapsed time: {elapsed:.4f}s\n")

        for i in range(len(faces)):
            print(f"[Face {i+1}]")
            print(f"  Bounding box : {faces[i].get('bbox')}")
            print(f"  Confidence   : {faces[i].get('confidence')}")
            print(f"  Landmarks    : {faces[i].get('landmarks')}\n")

    cpdef list run(self):
        cdef object image = self._load_image()

        cdef double start = time.time()
        cdef list faces = self.engine.detect(image)
        cdef double elapsed = time.time() - start

        self._log_results(faces, elapsed)

        if self.show:
            self._display(image)

        return faces


# =========================================================
# Detector (Orchestrator)
# =========================================================

cdef class Detector:
    cdef:
        object runner
        object worker

    def __cinit__(
        self,
        object image_path=None,
        object model=None,
        object runner=None,
        object worker=None,
        bint show=True,
    ):
        # ✅ INICIALIZAÇÃO OBRIGATÓRIA (ANTES DE QUALQUER RETURN)
        self.runner = None
        self.worker = None

        if worker is not None:
            self.worker = worker
            return

        if runner is not None:
            self.runner = runner
            return

        if image_path is None:
            raise ValueError("image_path is required when no runner/worker is provided")

        self.runner = BuiltinRunner(
            image_path,
            create_model(model),
            show,
        )

    cpdef object run(self):
        if self.worker is not None:
            return self.worker.execute()

        if self.runner is not None:
            return self.runner.run()

        raise RuntimeError("Detector is not properly configured")
