import cv2
from cv2.typing import MatLike
import numpy as np


class Setup:
    targets: list[str] = []

    def __init__(self, capture: str) -> None:
        self = capture
        Setup.targets.append(self)

    @classmethod
    def _check_captures(cls):
        assert len(cls.targets) >= 1, "None active captures"
        return

    @classmethod
    def capture(cls) -> MatLike | None:
        Setup._check_captures()

        cap = cv2.imread(cls.targets[0], cv2.IMREAD_COLOR)

        if cap is not None:
            h, w = cap.shape[:2]
            pts = np.array(
                [[100, 100], [w - 300, 300], [w - 100, h - 100], [100, h - 100]],
                np.int32,
            )

            pts = pts.reshape((-1, 1, 2))
            cv2.imshow("polygons", cap)
            print(f"Active captures {len(cls.targets)}")

            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return cap
            exit()
        else:
            pass
