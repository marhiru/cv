import time


class Timer:
    def __init__(self, start_time: float, *, verbose: bool = True) -> None:
        self.verbose = verbose
        self.start_time = start_time

    def exec_time(self) -> float:
        elapsed = time.time()
        result = elapsed - self.start_time

        if self.verbose:
            print(
                f"\n[\x1b[48;5;4m\x1b[38;5;0m  EXECUTION PERFORMANCE  \x1b[0m]\n"
                f"\n- \x1b[48;5;2m\x1b[38;5;0m TIME \x1b[0m | {result:.2f}s "
            )

        return result
