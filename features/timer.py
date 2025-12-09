import time


class Timer:
    def __init__(self, start_time: float, *, verbose: bool = True) -> None:
        self.verbose = verbose
        self.start_time = start_time

    def exec_time(self) -> float:
        elapsed = time.time()
        result = elapsed - self.start_time

        if self.verbose:
            print(f"[verbose] - [EXECUTION] {result:.2f}s | ")

        return result
