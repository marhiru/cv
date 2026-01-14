from typing import Any
from uniface.analyzer import FaceAnalyzer
from uniface.detection import RetinaFace
from uniface.recognition import ArcFace
from dataclasses import dataclass
from features.detect import Detector
import cv2
import matplotlib.pyplot as plt


@dataclass
class CustomWorker:
    image_secret: str
    image_cmp: str
    analyzer: Any

    def execute(self):
        image1 = cv2.imread(self.image_secret)
        image2 = cv2.imread(self.image_cmp)

        if image1 is None or image2 is None:
            raise FileNotFoundError("One or more images not found")

        faces1 = self.analyzer.analyze(image1)
        faces2 = self.analyzer.analyze(image2)

        print(f"Detected {len(faces1)} and {len(faces2)} faces")

        self._plot(image1, image2)

        if faces1 and faces2:
            similarity = faces1[0].compute_similarity(faces2[0])
            print(f"Similarity: {similarity:.4f}")
            return similarity

        raise RuntimeError("Could not detect faces")

    def _plot(self, image1, image2):
        _, axes = plt.subplots(1, 2, figsize=(10, 5))
        axes[0].imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
        axes[0].set_title("Image 1")
        axes[0].axis("off")

        axes[1].imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
        axes[1].set_title("Image 2")
        axes[1].axis("off")

        plt.tight_layout()
        plt.show()


def main() -> int:
    analyzer = FaceAnalyzer(
        detector=RetinaFace(confidence_threshold=0.5),
        recognizer=ArcFace(),
    )

    worker = CustomWorker(
        image_secret="./IMG_1451.jpeg",
        image_cmp="./IMG_1449.jpg",
        analyzer=analyzer,
    )

    detector = Detector(worker=worker)
    detector.run()

    return 0


if __name__ == "__main__":
    main()
